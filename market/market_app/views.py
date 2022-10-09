from django.views import View
from django.views.generic import TemplateView

# Поскольку меню категорий присутствует на всех страницах сайта, то
# вероятно, его лучше реализовать через контекст-процессор

# Зашлушка для меню категорий товара
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


class HomeView(TemplateView):
    """Главная страница"""
    template_name = 'index.html'
    extra_context = {'categories': categories}


class AboutView(TemplateView):
    """About"""
    template_name = 'about.html'
    extra_context = {'middle_title_left': 'About Megano',
                     'middle_title_right': 'About Us',
                     'categories': categories
                     }


# Заглушка для списка истории просмотров покупателя
history_view_list = [
    {
        'link': '#',
        'image': '/static/assets/img/content/home/card.jpg',
        'image_alt': 'card.jpg',
        'title': 'Corsair Carbide Series Arctic White Steel',
        'category': 'Games / XBox'
    },
    {
        'link': '#',
        'image': '/static/assets/img/content/home/card.jpg',
        'image_alt': 'card.jpg',
        'title': 'Corsair Carbide Series Arctic White Steel',
        'category': 'Games / XBox'
    },
    {
        'link': '#',
        'image': '/static/assets/img/content/home/card.jpg',
        'image_alt': 'card.jpg',
        'title': 'Corsair Carbide Series Arctic White Steel',
        'category': 'Games / XBox'
    },
    {
        'link': '#',
        'image': '/static/assets/img/content/home/card.jpg',
        'image_alt': 'card.jpg',
        'title': 'Corsair Carbide Series Arctic White Steel',
        'category': 'Games / XBox'
    },
    {
        'link': '#',
        'image': '/static/assets/img/content/home/card.jpg',
        'image_alt': 'card.jpg',
        'title': 'Corsair Carbide Series Arctic White Steel',
        'category': 'Games / XBox'
    },
]


class AccountView(TemplateView):
    """Account"""
    template_name = 'account.html'
    extra_context = {'middle_title_left': 'Личный кабинет',
                     'middle_title_right': 'Личный кабинет',
                     'categories': categories,
                     'history_view_list': history_view_list
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
    extra_context = {'middle_title_left': 'Catalog Megano', 'middle_title_right': 'Catalog'}


class CompareView(TemplateView):
    """Compare"""
    template_name = 'compare.html'
    extra_context = {'middle_title_left': 'Сравнение товаров', 'middle_title_right': 'Сравнение товаров'}


class ContactsView(TemplateView):
    """Contacts"""
    template_name = 'contacts.html'
    extra_context = {'middle_title_left': 'Contact Megano', 'middle_title_right': 'Contact'}


class HistoryOrderView(TemplateView):
    """History order"""
    template_name = 'historyorder.html'
    extra_context = {'middle_title_left': 'История заказов', 'middle_title_right': 'История заказов'}


class HistoryViewView(TemplateView):
    """History view"""
    template_name = 'historyview.html'
    extra_context = {'middle_title_left': 'История просмотра', 'middle_title_right': 'История просмотра'}


class OneOrderView(TemplateView):
    """One order"""
    template_name = 'oneorder.html'
    extra_context = {'middle_title_left': 'Заказ №200', 'middle_title_right': 'Заказ №200'}


class OrderView(TemplateView):
    """Order"""
    template_name = 'order.html'
    extra_context = {'middle_title_left': 'Оформление заказа', 'middle_title_right': 'Оформление заказа'}


class PaymentView(TemplateView):
    """Payment"""
    template_name = 'payment.html'
    extra_context = {'middle_title_left': 'Оплата', 'middle_title_right': 'Оплата'}


class PaymentSomeOneView(TemplateView):
    """Payment someone"""
    template_name = 'paymentsomeone.html'
    extra_context = {'middle_title_left': 'Оплата', 'middle_title_right': 'Оплата'}


class ProductView(TemplateView):
    """Product"""
    template_name = 'product.html'
    extra_context = {'middle_title_left': 'Megano Product', 'middle_title_right': 'Product'}


class ProfileView(TemplateView):
    """Profile"""
    template_name = 'profile.html'
    extra_context = {'middle_title_left': 'Профиль', 'middle_title_right': 'Профиль'}


class ProfileAvatarView(TemplateView):
    """Profile avatar"""
    template_name = 'profileAvatar.html'
    extra_context = {'middle_title_left': 'Профиль', 'middle_title_right': 'Профиль'}


class ProgressPaymentView(TemplateView):
    """Progress payment"""
    template_name = 'progressPayment.html'
    extra_context = {'middle_title_left': 'Ожидание оплаты', 'middle_title_right': 'Ожидание оплаты'}


class SaleView(TemplateView):
    """Sale"""
    template_name = 'sale.html'
    extra_context = {'middle_title_left': 'Megano Blog', 'middle_title_right': 'Blog'}


class ShopView(TemplateView):
    """Shop"""
    template_name = 'shop.html'
    extra_context = {'middle_title_left': 'About Megano', 'middle_title_right': 'About Us'}


class LoginOrRegisterView(View):
    """Login or register"""
    pass
