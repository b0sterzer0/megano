from django.shortcuts import render
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    """Главная страница"""
    template_name = 'index.html'


class AboutView(TemplateView):
    """About"""
    template_name = 'about.html'
    extra_context = {'middle_title_left': 'About Megano', 'middle_title_right': 'About Us'}


class AccountView(TemplateView):
    """Account"""
    template_name = 'account.html'
    extra_context = {'middle_title_left': 'Личный кабинет', 'middle_title_right': 'Личный кабинет'}


class CartView(TemplateView):
    """Cart"""
    template_name = 'cart.html'
    extra_context = {'middle_title_left': 'Корзина', 'middle_title_right': 'Корзина'}


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
    """Оrder"""
    template_name = 'order.html'
    extra_context = {'middle_title_left': 'Оформление заказа', 'middle_title_right': 'Оформление заказа'}


class PaymentView(TemplateView):
    """Payment"""
    template_name = 'payment.html'
    extra_context = {'middle_title_left': 'Оплата', 'middle_title_right': 'Оплата'}


# Пометка: исходные страницы payment.html и paymentsomeone.html почти ничем не отличаются.
# Подумать: может быть оставить только одну?
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


# Пометка: исходные страницы profile.html и profileAvatar.html почти ничем не отличаются.
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


# Пометка: shop.html очень похожа на about.html
class ShopView(TemplateView):
    """Shop"""
    template_name = 'shop.html'
    # extra_context = {'middle_title_left': 'Megano Blog', 'middle_title_right': 'Blog'}






