from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    full_name = models.CharField(
        max_length=200,
        default='',
        verbose_name='ФИО пользователя'
    )
    phone = models.CharField(
        max_length=12,
        default='+70000000000',
        verbose_name='Номер телелфона'
    )
    avatar = models.ImageField(
        upload_to='user_files/'
    )
    product_in_cart = models.IntegerField(
        default=0,
        verbose_name='Количество товара в корзине'
    )
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'profiles'
        verbose_name = 'profile'