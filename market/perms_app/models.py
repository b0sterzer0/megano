from django.db import models
from django.contrib.auth.models import User


class TestSaleModel(models.Model):
    sale_info = models.CharField(max_length=10)


class TestGoodProfileModel(models.Model):
    good_info = models.CharField(max_length=10)
    sale = models.ForeignKey(TestSaleModel, on_delete=models.CASCADE, blank=True, default=None)


class TestGoodModel(models.Model):
    good_name = models.CharField(max_length=10)
    good_profile = models.OneToOneField(TestGoodProfileModel, on_delete=models.CASCADE)


class TestUserProfileModel(models.Model):
    user_info = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class TestBasketModel(models.Model):
    goods = models.CharField(max_length=10)


class TestOrderDetailModel(models.Model):
    order_detail = models.CharField(max_length=10)


class TestOrderModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    basket = models.OneToOneField(TestBasketModel, on_delete=models.CASCADE)
    order_detail = models.OneToOneField(TestOrderDetailModel, on_delete=models.CASCADE)

