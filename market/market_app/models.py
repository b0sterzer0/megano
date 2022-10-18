from django.db import models


class Banner(models.Model):
    """ Модель рекламного баннера на главной странице сайта """
    title = models.CharField(max_length=50, verbose_name='заголовок')
    # Цены в рублях (без копеек)
    price = models.IntegerField(verbose_name='цена')
    # image = models.CharField(max_length=300, verbose_name='изображение')
    image = models.ImageField(upload_to='images/banners', verbose_name='изображение')
    image_alt = models.CharField(max_length=100, verbose_name='подсказка')
    link = models.CharField(max_length=300, verbose_name='url')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'баннер'
        verbose_name_plural = 'баннеры'
