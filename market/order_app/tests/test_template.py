from django.test import TestCase
from django.urls import reverse


class OrderTemplateTest(TestCase):
    def test_correct_template(self):
        resp = self.client.get(reverse('order'))

        self.assertTemplateUsed(resp, 'order.html')
