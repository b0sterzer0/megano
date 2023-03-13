from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache


class OrderTemplateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cache.set('order', {'full_name': 'test', 'delivery': 'express', 'city': 'test', 'address': 'test',
                            'phone': 'test', 'mail': 'test', 'pay': 'test'})

    def test_correct_template_in_order(self):
        step_1 = self.client.get(reverse('order_step_1'))
        step_2 = self.client.get(reverse('order_step_2'))
        step_3 = self.client.get(reverse('order_step_3'))
        step_4 = self.client.get(reverse('order_step_4'))
        cache.clear()

        self.assertTemplateUsed(step_1, 'order/order_step_1.html')
        self.assertTemplateUsed(step_2, 'order/order_step_2.html')
        self.assertTemplateUsed(step_3, 'order/order_step_3.html')
        self.assertTemplateUsed(step_4, 'order/order_step_4.html')
