from django.db.models import Min
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView

from compare_app.services import create_characteristics_dict
from market_app.banners import get_banners_list
from market_app.forms import ProductReviewForm, ProductsForm
from market_app.models import Seller, Product, SellerProduct
from market_app.product_history import HistoryViewOperations
from market_app.utils import (
    create_product_review,
    can_create_reviews,
    get_product_review_list,
    get_seller,
    get_count_product_reviews,
    get_count_product_in_cart,
    get_seller_products,
    get_catalog_product
)


# Поскольку меню категорий присутствует на всех страницах сайта, то
# вероятно, его лучше реализовать через контекст-процессор

# Заглушка для меню категорий товара


# Заглушка для списка элементов слайдера на главной странице
slider_items = [
                   {
                       'title1': 'Mavic Pro',
                       'title2': '5 ',
                       'title3': 'mini drone',
                       'text': 'Get the best phoneyou ever seen with modern Windows OS plus 70% Off this summer.',
                       'link': '#',
                       'image': '/static/assets/img/content/home/slider.png',
                       'image_alt': 'slider.png'
                   }
               ] * 3


class HomeView(TemplateView):
    """Главная страница"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.annotate(min_price=Min('seller_product__price'))
        context['banners_list'] = get_banners_list()
        context['slider_items'] = slider_items
        # необходимое количество можно взять из конфига
        context['popular_list'] = get_catalog_product()
        context['hot_offer_list'] = products
        context['limited_edition_list'] = products
        context['product_in_cart'] = get_count_product_in_cart(self.request)
        return context


class AboutView(TemplateView):
    """О нас"""
    template_name = 'about.html'
    extra_context = {
        'middle_title_left': 'О нас',
        'middle_title_right': 'О нас',
    }


class AccountView(TemplateView):
    """Личный кабинет"""
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with HistoryViewOperations(self.request.user) as history:
            history_view_list = history.products()[:3]
        context['middle_title_left'] = 'Личный кабинет'
        context['middle_title_right'] = 'Личный кабинет'
        context['active_menu'] = 'account'
        context['history_view_list'] = history_view_list
        return context


class CatalogView(TemplateView):
    """Каталог товаров"""
    template_name = 'catalog.html'
    extra_context = {
        'middle_title_left': 'Каталог товаров',
        'middle_title_right': 'Каталог товаров',
        'cards': get_catalog_product(),
    }


class ContactsView(TemplateView):
    """Контакты"""
    template_name = 'contacts.html'
    extra_context = {
        'middle_title_left': 'Контакты',
        'middle_title_right': 'Контакты',
    }


class HistoryOrderView(TemplateView):
    """История заказов пользователя"""
    template_name = 'historyorder.html'
    extra_context = {
        'middle_title_left': 'История заказов',
        'middle_title_right': 'История заказов',
        'active_menu': 'historyorder',
    }


class HistoryViewView(TemplateView):
    """История просмотров пользователя"""
    template_name = 'historyview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with HistoryViewOperations(self.request.user) as history:
            history_view_list = history.products()
        context['middle_title_left'] = 'История просмотра'
        context['middle_title_right'] = 'История просмотра'
        context['active_menu'] = 'historyview'
        context['history_view_list'] = history_view_list
        return context


class OneOrderView(TemplateView):
    """Информация о конкретном заказе"""
    template_name = 'oneorder.html'
    extra_context = {
        'middle_title_left': 'Заказ №200',
        'middle_title_right': 'Заказ №200',
    }


class OrderView(TemplateView):
    """Оформление заказа"""
    template_name = 'order.html'
    extra_context = {
        'middle_title_left': 'Оформление заказа',
        'middle_title_right': 'Оформление заказа',
    }


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
        context['reviews'] = get_product_review_list(product, page)
        context['can_create_reviews'] = can_create_reviews(product, self.request.user)
        context['num_review'] = get_count_product_reviews(product)
        context['images'] = product.images.all()
        context['sellers_price'] = get_seller_products(seller_products_list)
        context['min_price'] = min_price
        context['middle_title_left'] = product.name
        context['middle_title_right'] = product.name
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
            # Эту часть ввести после добавления загрузки фото с отзывами
            # images = request.FILES.getlist('images')
            create_product_review(product, request.user, description)

            return redirect('product', pk=product.id)
        return render(request, 'product.html', context=self.get_context_data(**kwargs))


class ProfileView(TemplateView):
    """Профиль пользователя"""
    template_name = 'profile.html'
    extra_context = {
        'middle_title_left': 'Профиль',
        'middle_title_right': 'Профиль',
        'active_menu': 'profile',
    }


class ProfileAvatarView(TemplateView):
    """Профиль пользователя с аватаром"""
    template_name = 'profileAvatar.html'
    extra_context = {
        'middle_title_left': 'Профиль',
        'middle_title_right': 'Профиль',
        'active_menu': 'profile',
    }


class SaleView(TemplateView):
    """Распродажа"""
    template_name = 'sale.html'
    extra_context = {
        'middle_title_left': 'Распродажа',
        'middle_title_right': 'Распродажа',
        'sale_list': get_catalog_product(),
    }


class ShopView(TemplateView):
    """Информация о магазине"""
    template_name = 'shop.html'
    extra_context = {
        'middle_title_left': 'О нас',
        'middle_title_right': 'О нас',
        'popular_list': get_catalog_product(),
    }


class LoginOrRegisterView(View):
    """Вход или регистрация"""
    pass


class SellerDetailView(DetailView):
    """Страница продавца"""
    model = Seller
    template_name = 'seller.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        seller = get_seller(pk)

        context['middle_title_left'] = seller.name
        context['middle_title_right'] = seller.name
        context['seller'] = seller
        context['products'] = get_seller_products(SellerProduct.objects.filter(seller=seller).select_related('product').all())

        #   TODO Заглушка для популярных товаров. Доделать, когда появится история покупок. Добавить все товары
        context['popular_list'] = get_seller_products(SellerProduct.objects.filter(seller=seller).select_related('product').all()[:2])  # get_popular_list_for_seller(pk)

        return context


class ProductFilter(View):

    def post(self, request):
        """Фильтр товаров"""
        cards = []
        products_form = ProductsForm(request.POST)
        if 'price' not in products_form.data:
            name_product = products_form.data['title']
            card = SellerProduct.objects.select_related('product').filter(product__name__contains=name_product)
            return render(request, 'catalog.html', context={'cards': get_seller_products(card)})
        price_product = products_form.data['price'].replace(';', ' ').split()
        name_product = products_form.data['title']
        cards_obj = SellerProduct.objects.select_related('product').filter(product__name__contains=name_product)
        cards_list = get_seller_products(cards_obj)
        for card in cards_list:
            if int(price_product[0]) <= card['price'] <= int(price_product[1]):
                cards.append(card)
        context = {
            'cards': cards
        }
        return render(request, 'catalog.html', context=context)
