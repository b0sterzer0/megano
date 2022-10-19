"""
Модуль для работы с баннерами, отображающимися на главной странице сайта.
На главной странице отображается три случайных баннера, баннеры кэшируются
на время, полученное из настроек сайта. При добавлении или удалении баннера
кэш сбрасывается.
"""
import random
from typing import List

from django.core.cache import cache
from django.db.models.signals import post_save, post_delete

from .models import Banner


def get_banners_cache_time() -> int:
    """
    Возвращает время кэширования баннеров на главной странице из настроек сайта
    """
    # Заглушка. Пока настройки не реализованы, время равно 10 минутам
    return 10 * 60


def get_banners_list() -> List:
    """
    Возвращает список из 3 случайных баннеров.
    Баннеры берутся из кэша. В случае отсутствия в кэше, берутся из базы.
    """

    def _get_banners_from_db() -> List:
        """ Возвращает список из 3 случайных баннеров из БД """
        try:
            return random.sample(list(Banner.objects.all()), 3)
        except ValueError:
            # На случай, если баннеров в базе меньше 3
            return []

    return cache.get_or_set('banners', _get_banners_from_db, get_banners_cache_time())


def reset_banners_cache(**kwargs):
    """ Очищает кэш баннеров """
    cache.delete('banners')


# Регистрируем функцию очистки кэша баннеров как функцию-приемник
# сигналов post_save и post_delete
post_save.connect(reset_banners_cache, sender=Banner)
post_delete.connect(reset_banners_cache, sender=Banner)
