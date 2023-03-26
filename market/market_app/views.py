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
    get_seller,
    get_count_product_reviews,
    get_count_product_in_cart,
    get_seller_products,
    get_catalog_product,
    get_selected_categories,
    get_catalog_products,
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


class AccountView(TemplateView):
    """Личный кабинет"""
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with HistoryViewOperations(self.request.user) as history:
            history_view_list = history.products()[:3]
        context['active_menu'] = 'account'
        context['history_view_list'] = history_view_list
        return context


class CatalogView(View):
    """Каталог товаров"""
    def get(self, request):
        return render(request, 'catalog.html', context=get_catalog_products(request))


class ContactsView(TemplateView):
    """Контакты"""
    template_name = 'contacts.html'


class HistoryOrderView(TemplateView):
    """История заказов пользователя"""
    template_name = 'historyorder.html'
    extra_context = {
        'active_menu': 'historyorder',
    }


class HistoryViewView(TemplateView):
    """История просмотров пользователя"""
    template_name = 'historyview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with HistoryViewOperations(self.request.user) as history:
            history_view_list = history.products()
        context['active_menu'] = 'historyview'
        context['history_view_list'] = history_view_list
        return context


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


class ProfileView(TemplateView):
    """Профиль пользователя"""
    template_name = 'profile.html'
    extra_context = {
        'active_menu': 'profile',
    }


class ProfileAvatarView(TemplateView):
    """Профиль пользователя с аватаром"""
    template_name = 'profileAvatar.html'
    extra_context = {
        'active_menu': 'profile',
    }


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
