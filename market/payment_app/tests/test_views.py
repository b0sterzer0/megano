from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from catalog_categories.models import Category
from market_app.models import Seller, Product, SellerProduct
from payment_app.models import TestBasketModel
from payment_app.views import post_method_for_payment_views
from api_for_payment_app.models import PaymentStatusModel


USERNAME = 'test'
PASSWORD = 'Asdfg54321'

## Перед запуском тестов, необходимо в отдельном терминале запустить сервер через py manage.py runserver, иначе
## у функции post_method_for_payment_views не получится отправить запрос к API


class PostMethodForPaymentViewTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        cls.category = Category.objects.create(title='телефоны', slug='phones', parent=None, activity=True)
        cls.product_1 = Product.objects.create(name='test_product_1', category=cls.category, slug='t_prod_1')
        cls.product_2 = Product.objects.create(name='test_product_2', category=cls.category, slug='t_prod_2')
        cls.product_3 = Product.objects.create(name='test_product_3', category=cls.category, slug='t_prod_3')
        cls.basket_1 = TestBasketModel.objects.create(user=cls.user, product=cls.product_1)
        cls.basket_2 = TestBasketModel.objects.create(user=cls.user, product=cls.product_1)
        cls.basket_3 = TestBasketModel.objects.create(user=cls.user, product=cls.product_1)
        cls.seller = Seller.objects.create(name=cls.user.username)
        cls.seller_product_1 = SellerProduct.objects.create(product=cls.product_1, seller=cls.seller, qty=1, price=10)
        cls.seller_product_2 = SellerProduct.objects.create(product=cls.product_2, seller=cls.seller, qty=1, price=10)
        cls.seller_product_3 = SellerProduct.objects.create(product=cls.product_3, seller=cls.seller, qty=1, price=10)
        cls.factory = RequestFactory()


    def setUp(self) -> None:
        self.login_user = self.client.login(username=USERNAME, password=PASSWORD)

    def test_check_setUp_data(self):
        self.assertTrue(self.login_user)
        self.assertTrue(self.category)
        self.assertTrue(self.product_1)
        self.assertTrue(self.product_2)
        self.assertTrue(self.product_3)
        self.assertTrue(self.basket_1)
        self.assertTrue(self.basket_2)
        self.assertTrue(self.basket_3)
        self.assertTrue(self.seller)
        self.assertTrue(self.seller_product_1)
        self.assertTrue(self.seller_product_2)
        self.assertTrue(self.seller_product_3)

    def test_standart_situation(self):
        response = self.factory.post('/payment/pay_my_card/', {'card_number': '1111 1112'})
        response.user = self.user
        status = post_method_for_payment_views(response)
        self.assertEqual(status, 'S400')

    def test_wrong_card_number(self):
        response = self.factory.post('/payment/pay_my_card/', {'card_number': '1111 1114'})
        response.user = self.user
        status = post_method_for_payment_views(response)
        self.assertEqual(status, 'S404')

    def test_wrong_card_balance(self):
        response = self.factory.post('/payment/pay_my_card/', {'card_number': '1111 1112'})
        response.user = self.user
        self.seller_product_1.price = 1000
        self.seller_product_1.save()
        status = post_method_for_payment_views(response)
        self.assertEqual(status, 'S403')

    def test_no_products_in_basket(self):
        TestBasketModel.objects.all().delete()
        response = self.client.post('/payment/pay_my_card/', {'card_number': '1111 1112'})
        self.assertEqual(response.status_code, 404)
