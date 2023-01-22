from django.core.cache import cache

from market_app.models import ProductReview, ProductReviewImage, Seller
from app_settings.utils import get_settings


def get_product_review_list(product):
    """
    Функция получает и возвращает список отзывов определенного товара.
    :param product: товар.
    :return: список отзывов определенного товара.
    """
    reviews = ProductReview.objects.filter(product=product).select_related('user').prefetch_related('images')
    return reviews


def create_product_review(product, user, description, images):
    """
    Функция создаёт отзыв к определенному товару.
    """
    review = ProductReview.objects.create(product=product,
                                          customer=user,
                                          description=description
                                          )
    for img in images:
        inst = ProductReviewImage(review=review, image=img)
        inst.save()


def get_count_product_reviews(product):
    """
    Функция получает и возвращает количество отзывов определенного товара.
    :param product: товар.
    :return: количество отзывов определенного товара.
    """
    num_review = ProductReview.objects.filter(product=product).count()
    return num_review


def get_seller(pk):
    """
    Функция получает время кэша данных продавца и
    возвращает кэш объекта продавца, если его нет, то предварительно загружает из БД
    и добавляет в кэш.
    :param pk: pk определенного продавца.
    :return: кэш объекта продавца.
    """
    settings_config = get_settings()
    seller_cache_time = settings_config['seller_cache_time']
    cache_key = f"seller_detail_{pk}"
    seller = cache.get(cache_key)
    if not seller:
        seller = Seller.objects.select_related('profile').get(pk=pk)
        cache.set(cache_key, seller, seller_cache_time)
    return seller


def get_popular_list_for_seller(pk):
    """
    Функция получает время кэша данных продавца и
    возвращает кэш объекта продавца, если его нет, то предварительно загружает из БД
    и добавляет в кэш.
    :param pk: pk определенного продавца.
    :return: список топ товаров продавца
    """
#   TODO Доделать после создания истории покупок
    pass
    # settings_config = get_settings()
    # sellers_products_top_cache_time = settings_config['sellers_products_top_cache_time']
    # cache_key = f"sellers_top_%s{pk}"
    # top_list = cache.get(cache_key)
    # if not top_list:
    #     top_list = Seller.objects.select_related('profile').get(pk=pk)
    #     cache.set(cache_key, top_list, sellers_products_top_cache_time)
    # return top_list
