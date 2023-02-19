import datetime

from django.db.models import Min
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.urls import reverse

from market_app.banners import get_banners_list
from market_app.forms import ProductReviewForm
from market_app.models import Seller, Product, ProductReviewImage, SellerProduct
from market_app.utils import (
    create_product_review,
    can_create_reviews,
    get_product_review_list,
    get_seller,
    get_count_product_reviews,
    get_popular_list_for_seller
)

# Поскольку меню категорий присутствует на всех страницах сайта, то
# вероятно, его лучше реализовать через контекст-процессор

# Заглушка для меню категорий товара
categories = [
    {
        'name': 'Компьютеры',
        'link': '#',
        'icon': '/static/assets/img/icons/departments/1.svg',
        'icon_alt': '1.svg'
    },
    {
        'name': 'Мониторы',
        'link': '#',
        'icon': '/static/assets/img/icons/departments/2.svg',
        'icon_alt': '2.svg'
    },
    {
        'name': 'Аксессуары',
        'link': '#',
        'icon': '/static/assets/img/icons/departments/3.svg',
        'icon_alt': '3.svg',
        'sub_categories': [
            {
                'name': 'Мышки',
                'link': '#',
                'icon': '/static/assets/img/icons/departments/4.svg',
                'icon_alt': '4.svg'
            },
            {
                'name': 'Коврики',
                'link': '#',
                'icon': '/static/assets/img/icons/departments/5.svg',
                'icon_alt': '5.svg'
            },
        ]
    },
]

date1 = datetime.date(year=2022, month=1, day=1)
date2 = datetime.date(year=2022, month=2, day=2)

# Заглушка для списка товаров
product_list = [
                   {
                       'link': '#',
                       'image': '/static/assets/img/content/home/card.jpg',
                       'image_alt': 'card.jpg',
                       'title': 'Corsair Carbide Series Arctic White Steel',
                       'category': 'Games / XBox',
                       'price': 100,
                       'price_old': 120,
                       'sale': '-60%',
                       'date': date1,
                       'date_to': date2,
                       'description': 'Lorem ipsum dolor sit amet consectetuer adipiscing elit sed diam nonummy nibh euismod tincid'
                   }
               ] * 20

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
    extra_context = {
        'categories': categories,
        'slider_items': slider_items,
        # необходимое количество можно взять из конфига
        'popular_list': product_list[:8],
        'hot_offer_list': product_list,
        'limited_edition_list': product_list
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Список баннеров
        context['banners_list'] = get_banners_list()
        # Далее будет получение других элементов контекста
        return context


class AboutView(TemplateView):
    """О нас"""
    template_name = 'about.html'
    extra_context = {
        'middle_title_left': 'О нас',
        'middle_title_right': 'О нас',
        'categories': categories
    }


class AccountView(TemplateView):
    """Личный кабинет"""
    template_name = 'account.html'
    extra_context = {
        'middle_title_left': 'Личный кабинет',
        'middle_title_right': 'Личный кабинет',
        'categories': categories,
        'history_view_list': product_list,
        'active_menu': 'account'
    }


class CartView(TemplateView):
    """Корзина"""
    template_name = 'cart.html'
    extra_context = {
        'middle_title_left': 'Корзина',
        'middle_title_right': 'Корзина',
        'categories': categories,
    }


class CatalogView(TemplateView):
    """Каталог товаров"""
    template_name = 'catalog.html'
    extra_context = {
        'middle_title_left': 'Каталог товаров',
        'middle_title_right': 'Каталог товаров',
        'categories': categories,
        'catalog_list': product_list,
    }


class CompareView(TemplateView):
    """Сравнение товаров"""
    template_name = 'compare.html'
    extra_context = {
        'middle_title_left': 'Сравнение товаров',
        'middle_title_right': 'Сравнение товаров',
        'categories': categories,
    }


class ContactsView(TemplateView):
    """Контакты"""
    template_name = 'contacts.html'
    extra_context = {
        'middle_title_left': 'Контакты',
        'middle_title_right': 'Контакты',
        'categories': categories,
    }


class HistoryOrderView(TemplateView):
    """История заказов пользователя"""
    template_name = 'historyorder.html'
    extra_context = {
        'middle_title_left': 'История заказов',
        'middle_title_right': 'История заказов',
        'categories': categories,
        'active_menu': 'historyorder',
    }


class HistoryViewView(TemplateView):
    """История просмотров пользователя"""
    template_name = 'historyview.html'
    extra_context = {
        'middle_title_left': 'История просмотра',
        'middle_title_right': 'История просмотра',
        'categories': categories,
        'history_view_list': product_list,
        'active_menu': 'historyview',
    }


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
        'categories': categories,
    }


class PaymentView(TemplateView):
    """Оплата по номеру карты"""
    template_name = 'payment.html'
    extra_context = {
        'middle_title_left': 'Оплата',
        'middle_title_right': 'Оплата',
        'categories': categories,
    }


class PaymentSomeOneView(TemplateView):
    """Оплата по номеру счета"""
    template_name = 'paymentsomeone.html'
    extra_context = {
        'middle_title_left': 'Оплата',
        'middle_title_right': 'Оплата',
        'categories': categories,
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
        context['reviews'] = get_product_review_list(product, page)
        context['can_create_reviews'] = can_create_reviews(product, self.request.user)
        context['num_review'] = get_count_product_reviews(product)
        context['images'] = product.images.all()
        seller_products_list = SellerProduct.objects.filter(product=product).all()
        context['sellers_price'] = seller_products_list
        context['min_price'] = seller_products_list.aggregate(Min('price'))
        context['middle_title_left'] = product.name
        context['middle_title_right'] = product.name
        context['review_form'] = ProductReviewForm()
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
        'categories': categories,
        'active_menu': 'profile',
    }


class ProfileAvatarView(TemplateView):
    """Профиль пользователя с аватаром"""
    template_name = 'profileAvatar.html'
    extra_context = {
        'middle_title_left': 'Профиль',
        'middle_title_right': 'Профиль',
        'categories': categories,
        'active_menu': 'profile',
    }


class ProgressPaymentView(TemplateView):
    """Ожидание оплаты"""
    template_name = 'progressPayment.html'
    extra_context = {
        'middle_title_left': 'Ожидание оплаты',
        'middle_title_right': 'Ожидание оплаты',
        'categories': categories,
    }


class SaleView(TemplateView):
    """Распродажа"""
    template_name = 'sale.html'
    extra_context = {
        'middle_title_left': 'Распродажа',
        'middle_title_right': 'Распродажа',
        'sale_list': product_list,
        'categories': categories,
    }


class ShopView(TemplateView):
    """Информация о магазине"""
    template_name = 'shop.html'
    extra_context = {
        'middle_title_left': 'О нас',
        'middle_title_right': 'О нас',
        'popular_list': product_list,
        'categories': categories,
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

        #   TODO Заглушка для популярных товаров. Доделать, когда появится история покупок. Добавить все товары
        context['popular_list'] = product_list[:4]  # get_popular_list_for_seller(pk)

        return context


class ProductFilter(View):

    def post(self, request):
        """Фильтр товаров"""
        cards = []
        products_form = ProductsForm(request.POST)
        if 'price' in products_form.data:
            price_product = products_form.data['price'].replace(';', ' ').split()
            name_product = products_form.data['title']
            cards_obj = SellerProduct.objects.filter(price__gt=price_product[0], price__lt=price_product[1])
            for temp_data in cards_obj:
                if name_product in temp_data.product.name:
                    cards.append(temp_data)
        else:
            name_product = products_form.data['title']
            card = Product.objects.filter(name__contains=name_product)
            return render(request, 'catalog.html', context={'cards': card})
        context = {
            'cards': cards
        }
        return render(request, 'catalog.html', context=context)
