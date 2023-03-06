from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
from django.contrib import auth
from django.test.client import RequestFactory

from app_login.models import Profile
from order_app.utils import add_data_in_order_cache, delete_data_from_order_cache
from app_cart.models import AnonimCart
from market_app.models import Category, Product, Seller, SellerProduct


class OrderStepOneViewTest(TestCase):
    USERNAME = 'test'
    PASSWORD = 'Asdfg54321'
    EMAIL = 'test@mail.ru'
    FULL_NAME = 'test test test'
    PHONE = '1111111111'
    AVATAR = 'test'

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username=cls.USERNAME, email=cls.EMAIL)
        user.set_password(cls.PASSWORD)
        user.save()
        cls.profile = Profile.objects.create(user=user,
                                             full_name=cls.FULL_NAME,
                                             phone=cls.PHONE,
                                             avatar=cls.AVATAR)

    def test_post_method_user_is_not_authenticated(self):
        self.client.logout()
        resp = self.client.post(reverse('order_step_1'), {'name': 'test test test',
                                                          'phone': self.PHONE,
                                                          'mail': 'another_test@mail.ru',
                                                          'password': self.PASSWORD,
                                                          'passwordReply': self.PASSWORD})
        user = auth.get_user(self.client)
        users_queryset = User.objects.filter(id=user.id)

        self.assertTrue(user.is_authenticated)
        self.assertTrue(users_queryset)

    def setUp(self) -> None:
        self.client.login(username=self.USERNAME, password=self.PASSWORD)

    def test_get_method_user_is_authenticated(self):
        resp = self.client.get(reverse('order_step_1'))
        context = resp.context

        self.assertEqual(context['full_name'], self.FULL_NAME)
        self.assertEqual(context['phone'], self.PHONE)
        self.assertEqual(context['email'], self.EMAIL)

    def test_post_method(self):
        resp = self.client.post(reverse('order_step_1'), {'name': self.FULL_NAME,
                                                          'phone': self.PHONE,
                                                          'mail': self.EMAIL})
        order_dict = cache.get('order')

        self.assertTrue(order_dict)
        self.assertEqual(order_dict['full_name'], self.FULL_NAME)
        self.assertRedirects(resp, '/order/step2/')


class OrderStepTwoViewTest(TestCase):
    DELIVERY = 'ordinary'
    CITY = 'Воронеж'
    ADDRESS = 'test address'

    def test_get_method(self):
        resp = self.client.get(reverse('order_step_2'))

        self.assertEqual(resp.status_code, 200)

    def test_get_method_with_params(self):
        params_dict = {'delivery': self.DELIVERY, 'city': self.CITY, 'address': self.ADDRESS}
        add_data_in_order_cache(**params_dict)

        resp = self.client.get(reverse('order_step_2'))
        delete_data_from_order_cache(*params_dict.keys())
        context = resp.context

        self.assertIsNotNone(context)
        self.assertEqual(context['city'], self.CITY)

    def test_post_method(self):
        resp = self.client.post(reverse('order_step_2'), {'delivery': self.DELIVERY,
                                                          'city': self.CITY,
                                                          'address': self.ADDRESS})
        order_dict = cache.get('order')

        self.assertEqual(order_dict['address'], self.ADDRESS)
        self.assertRedirects(resp, '/order/step3/')


class OrderStepThreeViewTest(TestCase):
    PAY = 'someone'

    def test_get_method(self):
        resp = self.client.get(reverse('order_step_3'))

        self.assertEqual(resp.status_code, 200)

    def test_get_method_with_params(self):
        add_data_in_order_cache(**{'pay': self.PAY})
        resp = self.client.get(reverse('order_step_3'))
        delete_data_from_order_cache(*['pay'])
        context = resp.context

        self.assertIsNotNone(context)
        self.assertEqual(context['pay'], self.PAY)

    def test_post_method(self):
        resp = self.client.post(reverse('order_step_3'), {'pay': self.PAY})
        order_dict = cache.get('order')

        self.assertEqual(order_dict['pay'], self.PAY)
        self.assertRedirects(resp, '/order/step4/')


# class OrderStepFourViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(username='test user', password='Asdfg54321')
#         cls.profile = Profile.objects.create(user=cls.user, full_name='test test test', phone='888888')
#         cls.category = Category.objects.create(title='телефоны', slug='phones', parent=None, activity=True)
#         cls.product_1 = Product.objects.create(name='test_product_1', category=cls.category, slug='t_prod_1')
#         cls.product_2 = Product.objects.create(name='test_product_2', category=cls.category, slug='t_prod_2')
#         cls.seller = Seller.objects.create(name='test', profile=cls.profile, description='test')
#         cls.seller_product_1 = SellerProduct.objects.create(product=cls.product_1, seller=cls.seller, qty=1, price=10)
#         cls.seller_product_2 = SellerProduct.objects.create(product=cls.product_2, seller=cls.seller, qty=1, price=10)
#         # cls.factory = RequestFactory()
#
#     def test_get_method_user_is_not_authenticate(self):
#         self.client.logout()
#         resp = self.client.post(reverse('order_step_4'))
#         card = AnonimCart(resp)
#         card.add_product(self.product_1.id, self.seller_product_1.price)
#         card.add_product(self.product_2.id, self.seller_product_2.price)
#         resp = self.client.get(reverse('order_step_4'))
#
#         self.assertEqual(resp.status_code, 200)


