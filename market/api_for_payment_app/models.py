from django.db import models


class CardModel(models.Model):
    card_number = models.CharField(max_length=9, verbose_name='номер карты')
    balance = models.FloatField(verbose_name='баланс карты')

    class Meta:
        verbose_name = 'номер карты'
        verbose_name_plural = 'номера карт'

    def __str__(self):
        return self.card_number


class PaymentStatusModel(models.Model):
    status_code = models.CharField(max_length=5, verbose_name='код статуса')
    status_description = models.CharField(max_length=100, verbose_name='описание статуса')

    class Meta:
        verbose_name = 'статус оплаты'
        verbose_name_plural = 'статусы оплаты'

    def __str__(self):
        return self.status_code
