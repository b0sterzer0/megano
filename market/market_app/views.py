import datetime

from django.views import View
from django.views.generic import TemplateView

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
        'description': 'Lorem ipsum dolor sit amet consectetuer adipiscing elit sed diam nonummy nibh euismod tincid unt ut laoreet dolore'
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

# Заглушка для списка баннеров на главной странице
banners_list = [
    {
        'link': '#',
        'title': 'Video Cards',
        'price': '$199',
        'image': '/static/assets/img/content/home/videoca.png',
        'image_alt': 'videoca.png'
    }
] * 3


class HomeView(TemplateView):
    """Главная страница"""
    template_name = 'index.html'
    extra_context = {'categories': categories,
                     'slider_items': slider_items,
                     'banners_list': banners_list}


class AboutView(TemplateView):
    """About"""
    template_name = 'about.html'
    extra_context = {'middle_title_left': 'About Megano',
                     'middle_title_right': 'About Us',
                     'categories': categories
                     }


class AccountView(TemplateView):
    """Account"""
    template_name = 'account.html'
    extra_context = {'middle_title_left': 'Личный кабинет',
                     'middle_title_right': 'Личный кабинет',
                     'categories': categories,
                     'history_view_list': product_list
                     }


class CartView(TemplateView):
    """Cart"""
    template_name = 'cart.html'
    extra_context = {'middle_title_left': 'Корзина',
                     'middle_title_right': 'Корзина',
                     'categories': categories
                     }


class CatalogView(TemplateView):
    """Catalog"""
    template_name = 'catalog.html'
    extra_context = {'middle_title_left': 'Catalog Megano',
                     'middle_title_right': 'Catalog'}


class CompareView(TemplateView):
    """Compare"""
    template_name = 'compare.html'
    extra_context = {'middle_title_left': 'Сравнение товаров',
                     'middle_title_right': 'Сравнение товаров'}


class ContactsView(TemplateView):
    """Contacts"""
    template_name = 'contacts.html'
    extra_context = {'middle_title_left': 'Contact Megano',
                     'middle_title_right': 'Contact'}


class HistoryOrderView(TemplateView):
    """History order"""
    template_name = 'historyorder.html'
    extra_context = {'middle_title_left': 'История заказов',
                     'middle_title_right': 'История заказов'}


class HistoryViewView(TemplateView):
    """History view"""
    template_name = 'historyview.html'
    extra_context = {'middle_title_left': 'История просмотра',
                     'middle_title_right': 'История просмотра'}


class OneOrderView(TemplateView):
    """One order"""
    template_name = 'oneorder.html'
    extra_context = {'middle_title_left': 'Заказ №200',
                     'middle_title_right': 'Заказ №200'}


class OrderView(TemplateView):
    """Order"""
    template_name = 'order.html'
    extra_context = {'middle_title_left': 'Оформление заказа',
                     'middle_title_right': 'Оформление заказа'}


class PaymentView(TemplateView):
    """Payment"""
    template_name = 'payment.html'
    extra_context = {'middle_title_left': 'Оплата',
                     'middle_title_right': 'Оплата'}


class PaymentSomeOneView(TemplateView):
    """Payment someone"""
    template_name = 'paymentsomeone.html'
    extra_context = {'middle_title_left': 'Оплата',
                     'middle_title_right': 'Оплата'}


class ProductView(TemplateView):
    """Product"""
    template_name = 'product.html'
    extra_context = {'middle_title_left': 'Megano Product',
                     'middle_title_right': 'Product'}


class ProfileView(TemplateView):
    """Profile"""
    template_name = 'profile.html'
    extra_context = {'middle_title_left': 'Профиль',
                     'middle_title_right': 'Профиль'}


class ProfileAvatarView(TemplateView):
    """Profile avatar"""
    template_name = 'profileAvatar.html'
    extra_context = {'middle_title_left': 'Профиль',
                     'middle_title_right': 'Профиль'}


class ProgressPaymentView(TemplateView):
    """Progress payment"""
    template_name = 'progressPayment.html'
    extra_context = {'middle_title_left': 'Ожидание оплаты',
                     'middle_title_right': 'Ожидание оплаты'}


class SaleView(TemplateView):
    """Sale"""
    template_name = 'sale.html'
    extra_context = {'middle_title_left': 'Megano Blog',
                     'middle_title_right': 'Blog',
                     'categories': categories,
                     'cards_blog': product_list,
                     }


class ShopView(TemplateView):
    """Shop"""
    template_name = 'shop.html'
    extra_context = {'middle_title_left': 'About Megano',
                     'middle_title_right': 'About Us',
                     'categories': categories,
                     'popular_products': product_list,
                     }


class LoginOrRegisterView(View):
    """Login or register"""
    pass
