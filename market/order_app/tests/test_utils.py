from django.core.cache import cache
from django.test import TestCase

from order_app.utils import add_data_in_order_cache, delete_data_from_order_cache


class AddDataInOrderCacheTest(TestCase):
    TEST_1 = 'test test test'
    TEST_2 = '0000000000'
    TEST_3 = 'test@mail.ru'

    def test_ordinary_situation(self):
        data_dict = {'test_1': self.TEST_1,
                     'test_2': self.TEST_2,
                     'test_3': self.TEST_3}
        add_data_in_order_cache(**data_dict)
        order_dict = cache.get('order')

        self.assertIsNotNone(order_dict)
        self.assertEqual(order_dict['test_3'], 'test@mail.ru')


class DeleteDataFromOrderCacheTest(TestCase):
    def test_ordinary_situation(self):
        param_keys = ['test_1', 'test_2', 'test_3']
        delete_data_from_order_cache(*param_keys)
        order_dict = cache.get('order')

        self.assertIsNotNone(order_dict)
        self.assertNotIn('test_2', order_dict.keys())

