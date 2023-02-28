from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from app_login.models import Profile


class OrderViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', email='test@mail.ru')
        user.set_password('Asdfg54321')
        user.save()
        cls.profile = Profile.objects.create(user=user,
                                             full_name='test test test',
                                             phone='1111111111',
                                             avatar='test')

    def setUp(self) -> None:
        self.client.login(username='test', password='Asdfg54321')

    def test_get_method_user_is_authenticated(self):
        resp = self.client.get(reverse('order'))
        context = resp.context

        self.assertEqual(context['full_name'], 'test test test')
        self.assertEqual(context['phone'], '1111111111')
        self.assertEqual(context['email'], 'test@mail.ru')
