from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache

from app_login.models import Profile
from order_app.utils import add_data_in_order_cache, delete_data_from_order_cache


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


class OrderStepFourViewTest(TestCase):
    def test_get_method(self):
        resp = self.client.get(reverse('order_step_4'))

        self.assertEqual(resp.status_code, 200)
