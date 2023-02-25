from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from market_app.models import Seller, Product, SellerProduct, Category
from app_login.models import Profile
from payment_app.models import TestBasketModel
from payment_app.views import post_method_for_payment_views


USERNAME = 'test'
PASSWORD = 'Asdfg54321'

## Перед запуском тестов, необходимо в отдельном терминале запустить сервер через py manage.py runserver, иначе
## у функции post_method_for_payment_views не получится отправить запрос к API
## Также, в БД должны существовать модели CardModel и PaymentStatusModel


class PostMethodForPaymentViewTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        cls.category = Category.objects.create(title='телефоны', slug='phones', parent=None, activity=True)
        cls.product = Product.objects.create(name='test_product_1', category=cls.category, slug='t_prod_1')
        for _ in range(3):
            TestBasketModel.objects.create(user=cls.user, product=cls.product)
        cls.profile = Profile.objects.create(user=cls.user, full_name='test test test', phone='888888')
        cls.seller = Seller.objects.create(name=cls.user.username, profile=cls.profile, description='test')
        cls.seller_product = SellerProduct.objects.create(product=cls.product, seller=cls.seller, qty=1, price=10)
        cls.factory = RequestFactory()


    def setUp(self) -> None:
        self.login_user = self.client.login(username=USERNAME, password=PASSWORD)


    def test_standart_situation(self):
        response = self.factory.post('/payment/pay_my_card/', {'card_number': '1111 1112'})
        response.user = self.user
        status = post_method_for_payment_views(response)
        self.assertEqual(status['status']['status_code'], 'S200')

    def test_wrong_card_number(self):
        response = self.factory.post('/payment/pay_my_card/', {'card_number': '1111 1114'})
        response.user = self.user
        status = post_method_for_payment_views(response)
        self.assertEqual(status['status']['status_code'], 'S404')

    def test_wrong_card_balance(self):
        response = self.factory.post('/payment/pay_my_card/', {'card_number': '1111 1112'})
        response.user = self.user
        self.seller_product.price = 1000
        self.seller_product.save()
        status = post_method_for_payment_views(response)
        self.assertEqual(status['status']['status_code'], 'S403')

    def test_no_products_in_basket(self):
        TestBasketModel.objects.all().delete()
        response = self.factory.post('/payment/pay_my_card/', {'card_number': '1111 1112'})
        response.user = self.user
        status = post_method_for_payment_views(response)
        self.assertEqual(status['status']['status_code'], 'S000')
