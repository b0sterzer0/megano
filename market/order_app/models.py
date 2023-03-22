from django.contrib.auth.models import User
from django.db import models


class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='заказчик')
    json_order_data = models.JSONField(verbose_name='данные заказа в формате JSON')
    activity = models.BooleanField(default=True, verbose_name='статус активности')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.user} - {self.activity}'
