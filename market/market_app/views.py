from django.db.models import Min
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView

from compare_app.services import create_characteristics_dict
from market_app.banners import get_banners_list
from market_app.forms import ProductReviewForm
from market_app.models import Seller, Product, SellerProduct
from market_app.product_history import HistoryViewOperations
from market_app.utils import (
    create_product_review,
    can_create_reviews,
    get_product_review_list_by_page,
    get_product_list_by_page,
    get_seller,
    get_count_product_reviews,
    get_count_product_in_cart,
    get_seller_products,
    get_catalog_product,
    get_min_cards,
    get_selected_categories,
    sort_list
)



class HomeView(TemplateView):
    """Главная страница"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.annotate(min_price=Min('sellers_products__price'))
        context['selected_categories'] = get_selected_categories()
        context['slider_banners'] = get_banners_list()
        # необходимое количество можно взять из конфига
        context['popular_list'] = get_catalog_product()
        context['hot_offer_list'] = products
        context['limited_edition_list'] = products
        context['product_in_cart'] = get_count_product_in_cart(self.request)
        return context


class AboutView(TemplateView):
    """О нас"""
    template_name = 'about.html'


class CatalogView(View):
    """Каталог товаров"""
    def get(self, request):
        cards = []
        price, title, stock, sort_by, page = request.GET.get('price'), request.GET.get('title'), \
            request.GET.get('stock'), request.GET.get('sort_by'), request.GET.get('page')
        if not price and not title:
            cards = get_catalog_product()
            sort_list(cards, sort_by)
            cards = get_product_list_by_page(cards, page)
            context = {
                'cards': cards,
                'sort_by': sort_by
            }
            return render(request, 'catalog.html', context=context)
        if not price:
            name_product = title
            cards_obj = SellerProduct.objects.select_related('product').filter(product__name__contains=name_product)
            get_min_cards(cards, cards_obj)
            sort_list(cards, sort_by)
            cards = get_product_list_by_page(cards, page)
            add_url = f'title={title}'
            return render(request, 'catalog.html', context={'cards': cards, 'add_url': add_url, 'sort_by': sort_by})
        price_product = price.replace(';', ' ').split()
        cards_obj = SellerProduct.objects.select_related('product').filter(product__name__contains=title)
        if stock:
            cards_obj = SellerProduct.objects.select_related('product').filter(product__name__contains=title).filter(
                qty__gt=0)
        cards_list = get_seller_products(cards_obj)
        for card in cards_list:
            if int(price_product[0]) <= card['price'] <= int(price_product[1]):
                cards.append(card)
        for card_1 in cards_list:
            for card_2 in cards:
                if card_1['name'] == card_2['name'] and card_1['price'] < card_2['price']:
                    cards.pop(cards.index(card_2))
        add_url = f'price={price_product[0]}%3B{price_product[1]}&title={title}'
        cards = get_product_list_by_page(cards, page)
        sort_list(cards, sort_by)
        context = {
            'cards': cards,
            'add_url': add_url,
            'sort_by': sort_by
        }
        return render(request, 'catalog.html', context=context)

    def post(self, request):
        """Фильтр товаров"""
        cards = []
        products_form = ProductsForm(request.POST)
        if 'price' not in products_form.data:
            name_product = products_form.data['title']
            cards_obj = SellerProduct.objects.filter(product__name__contains=name_product)
            cards_list = get_seller_products(cards_obj)
            for card in cards_list:
                cards.append(card)
            for card_1 in cards_list:
                for card_2 in cards:
                    if card_1['name'] == card_2['name'] and card_1['price'] < card_2['price']:
                        cards.pop(cards.index(card_2))
            return render(request, 'catalog.html', context={'cards': cards})
        price_product = products_form.data['price'].replace(';', ' ').split()
        name_product = products_form.data['title']
        cards_obj = SellerProduct.objects.filter(product__name__contains=name_product)
        cards_list = get_seller_products(cards_obj)
        for card in cards_list:
            if int(price_product[0]) <= card['price'] <= int(price_product[1]):
                cards.append(card)
        for card_1 in cards_list:
            for card_2 in cards:
                if card_1['name'] == card_2['name'] and card_1['price'] < card_2['price']:
                    cards.pop(cards.index(card_2))
        context = {
            'cards': cards
        }
        return render(request, 'catalog.html', context=context)


class ContactsView(TemplateView):
    """Контакты"""
    template_name = 'contacts.html'


class ProductView(DetailView):
    """Просмотр информации о конкретном товаре"""
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        page = self.request.GET.get('page')
        seller_products_list = SellerProduct.objects.filter(product=product).all()
        min_price = min(get_seller_products(seller_products_list), key=lambda i: int(i['price']))['price']
        context['reviews'] = get_product_review_list_by_page(product, page)
        context['can_create_reviews'] = can_create_reviews(product, self.request.user)
        context['num_review'] = get_count_product_reviews(product)
        context['images'] = product.images.all()
        context['sellers_price'] = get_seller_products(seller_products_list)
        context['min_price'] = min_price
        context['review_form'] = ProductReviewForm()
        context['product_id'] = product.id
        context['product_in_cart'] = get_count_product_in_cart(self.request)
        context['characteristics'] = create_characteristics_dict(product)
        if self.request.user.is_authenticated:
            with HistoryViewOperations(self.request.user) as history:
                history.add_product(product)
        return context

    def post(self, request, *args, **kwargs):
        review_form = ProductReviewForm(request.POST)
        product = self.get_object()

        if review_form.is_valid():
            description = review_form.cleaned_data['description']
            create_product_review(product, request.user, description)

            return redirect('product', pk=product.id)
        return render(request, 'product.html', context=self.get_context_data(**kwargs))


class SaleView(TemplateView):
    """Распродажа"""
    template_name = 'sale.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = get_catalog_product()
        return context


class ShopView(TemplateView):
    """Информация о магазине"""
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = get_catalog_product()
        return context


class SellerDetailView(DetailView):
    """Страница продавца"""
    model = Seller
    template_name = 'seller.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        seller = get_seller(pk)
        context['seller'] = seller
        context['products'] = get_seller_products(
            SellerProduct.objects.filter(seller=seller).select_related('product').all())

        #   TODO Заглушка для популярных товаров. Доделать, когда появится история покупок. Добавить все товары
        context['popular_list'] = get_seller_products(
            SellerProduct.objects.filter(seller=seller).select_related('product').all()[:2])

        return context
