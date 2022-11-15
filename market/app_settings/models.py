from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """Модель настроек сайта"""
    site_name = models.CharField(max_length=255, verbose_name=_('Название сайта'))
    phone_number1 = models.CharField(max_length=255, verbose_name=_('Номер телефона 1'))
    phone_number2 = models.CharField(max_length=255, verbose_name=_('Номер телефона 2'))
    address = models.CharField(max_length=255, verbose_name=_('Адрес'))
    banner_number = models.PositiveSmallIntegerField(verbose_name=_('Количество баннеров'))
    stopping_sales = models.BooleanField(default=False, verbose_name=_('Остановка продаж'))
    banner_cache_time = models.PositiveIntegerField(verbose_name=_('Кэш баннеров'))
    total_cache_time = models.PositiveIntegerField(verbose_name=_('Общий кэш'))

    def __str__(self):
        return 'Настройки сайта'

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Настройка сайта')
        verbose_name_plural = _('Настройки сайта')
