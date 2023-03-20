import json

from django.test import TestCase
from django.contrib.auth.models import User

from payment_app.utils import create_payment_status_dict, change_payment_status_in_order, get_total_price
from api_for_payment_app.models import PaymentStatusModel
from order_app.models import OrderModel


class CreatePaymentStatusDictFuncTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PaymentStatusModel.objects.create(status_code='S200', status_description='test desc')

    def test_ordinary_situation(self):
        status_dict = create_payment_status_dict('S200')

        self.assertEqual(status_dict['status']['status_code'], 'S200')


class ChangePaymentStatusInOrderFuncTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test user')
        json_order_data = json.dumps({'t_price': 1000, 'products_list': [{'test': 'test'}, {'test_2': 'test'}],
                                      'order_dict': {'payment_status': 'Не оплачено'}})
        cls.order_object = OrderModel.objects.create(user=user, json_order_data=json_order_data)

    def test_ordinary_situation(self):
        change_payment_status_in_order(self.order_object.id)
        order_obj = OrderModel.objects.all().first()
        order_data = json.loads(order_obj.json_order_data)

        self.assertTrue(order_data['order_dict']['payment_status'], 'Оплачено')


class GetTotalPriceFuncTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test user')
        json_order_data = json.dumps({'t_price': 1000, 'products_list': [{'test': 'test'}, {'test_2': 'test'}],
                                      'order_dict': {'payment_status': 'Не оплачено'}})
        cls.order_object = OrderModel.objects.create(user=user, json_order_data=json_order_data)

    def test_ordinary_situation(self):
        t_price = get_total_price(self.order_object.id)

        self.assertEqual(t_price, 1000)
