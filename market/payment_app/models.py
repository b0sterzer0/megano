from django.db import models
from django.contrib.auth.models import User

from market_app.models import Product


class TestBasketModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return self.user.username
