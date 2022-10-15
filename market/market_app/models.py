from django.db import models


class Banner(models.Model):
    """ Баннер """
    title = models.CharField(max_length=50, verbose_name='заголовок')
    # Максимальная цена 999 999 999.99
    price = models.DecimalField(max_digits=11, decimal_places=2, verbose_name='цена')
    image = models.CharField(max_length=300, verbose_name='изображение')
    image_alt = models.CharField(max_length=100, verbose_name='подсказка')
    link = models.CharField(max_length=300, verbose_name='url')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'баннер'
        verbose_name_plural = 'баннеры'
