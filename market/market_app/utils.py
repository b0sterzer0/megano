from django.core.cache import cache
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator, Page

from app_cart.models import AnonimCart
from app_login.models import Profile
from app_settings.utils import get_setting_from_bd
from market_app.models import Product, ProductReview, Seller, SellerProduct


def make_paginator_from_list(lst, num_page, page):
    """
    Функция получает список, разбивает на страницы и возвращает объекты с заданной страницы
    :param lst: начальный список.
    :param num_page: всего количество страниц.
    :param page: номер страницы для возврата объектов.
    :return: список отзывов определенного товара заданной страницы.
    """
    paginator = Paginator(lst, num_page)
    page = page
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        objects = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        objects = paginator.page(paginator.num_pages)
    return objects


def get_product_review_list_by_page(product, page):
    """
    Функция получает товар и номер страницы, загружает из БД список отзывов для данного товара
    и количество отзывов на странице, отправляет данные в функцию make_paginator_from_list(),
    возвращает список отзывов определенного товара для заданной страницы.
    :param product: товар.
    :param page: номер страницы для возврата отзывов.
    :return: список отзывов определенного товара заданной страницы.
    """

    reviews_list = ProductReview.objects.filter(product=product).select_related('customer').order_by('-date')
    num_reviews = get_setting_from_bd('num_reviews_per_page')
    reviews = make_paginator_from_list(reviews_list, num_reviews, page)
    return reviews


def get_product_list_by_page(products_list, page):
    """
    Функция получает полный список товаров и возвращает список товаров для определенной стриницы.
    :param products_list: изначальный список товаров.
    :param page: номер страницы для возврата товаров.
    :return: список товаров для заданной страницы.
    """

    num_products_per_page = get_setting_from_bd('num_products_per_page')
    products = make_paginator_from_list(products_list, num_products_per_page, page)
    return products


def can_create_reviews(product, user):
    """
    Функция проверяет, есть ли у товара отзыв от определенного пользователя,
    если есть - возвращает False, иначе - True
    """
    if user.is_authenticated:
        reviews = ProductReview.objects.filter(product=product).filter(customer=user).all()
        if reviews:
            return False
        return True


def create_product_review(product, user, description):
    """
    Функция создаёт отзыв к определенному товару.
    """
    ProductReview.objects.create(product=product,
                                 customer=user,
                                 description=description
                                 )
    # Эту часть ввести после добавления загрузки фото с отзывами
    # for img in images:
    #     ProductReviewImage.objects.create(review=review, image=img)


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
    seller_cache_time = get_setting_from_bd('seller_cache_time')
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


def get_count_product_in_cart(request):
    """
    Функция для вычисления количества товаров в корзине пользователя
    """
    if request.user.is_authenticated:
        count_in_cart = [count.product_in_cart for count in
                         Profile.objects.filter(user_id=request.user.id).only('product_in_cart')]
        return count_in_cart[0]
    else:
        cart = AnonimCart(request)
        return cart.get_count_product_in_cart()


def get_price(product_obj):
    """
    Функция принимает товар и просчитывает цену с учётом скидки
    """
    products_obj = []
    for product_form_seller_product in SellerProduct.objects.all():
        if product_form_seller_product.product.name == product_obj.name:
            products_obj.append(product_form_seller_product)
    price_after_discount = products_obj[0]
    for product in products_obj:
        if product.discount:
            product.price = round(float(product.price) * (1 - product.discount.discount / 100), 2)
        if product.price < price_after_discount.price:
            price_after_discount = product
    return price_after_discount.price


def get_catalog_product():
    """
    Функция формирует удобный список с информацией для товаров на основе class Product
    """
    products_list = []
    queryset = Product.objects.all()
    for product_obj in queryset:
        year = 0
        values = product_obj.values.all()
        for value in values:
            if value.characteristic.characteristic_name.lower() == 'год выпуска':
                year = int(value.value)
        products_list.append(
            {
                'id': product_obj.id,
                'link': product_obj.slug,
                'images': {'first': {'image': {'url': product_obj.images.first().image.url}}},
                'image_alt': {'first': {'image_alt': product_obj.images.first().image_alt}},
                'name': product_obj.name,
                'category': product_obj.category,
                'price': get_price(product_obj),
                'description': product_obj.description,
                'count_reviews': get_count_product_reviews(product_obj),
                'year': year,
                'rating': product_obj.productpurchases.num_purchases,
            }
        )
    return products_list


def get_seller_products(queryset):
    """
    Функция формирует удобный список с информацией для товаров на основе class SellerProduct
    """
    products_list = []
    year = 0
    for product in queryset:
        values = product.product.values.all()
        for value in values:
            if value.characteristic.characteristic_name.lower() == 'год':
                year = int(value.value)
        if product.discount:
            sale = product.discount
            products_list.append(
                {
                    'id': product.product_id,
                    'seller': product.seller.name,
                    'seller_id': product.seller.id,
                    'link': product.product.slug,
                    'images': {'first': {'image': {'url': product.product.images.first().image.url}}},
                    'image_alt': {'first': {'image_alt': product.product.images.first().image_alt}},
                    'name': product.product.name,
                    'category': product.product.category,
                    'price': round(float(product.price) * (1 - sale.discount / 100), 2),
                    'price_old': product.price,
                    'sale': sale.discount,
                    'date': sale.start_date,
                    'date_to': sale.end_date,
                    'description': product.product.description,
                    'count_reviews': get_count_product_reviews(product.product),
                    'year': year,
                    'rating': product.product.productpurchases.num_purchases,
                }
            )
        else:
            products_list.append(
                {
                    'id': product.product_id,
                    'seller': product.seller.name,
                    'seller_id': product.seller.id,
                    'link': product.product.slug,
                    'images': {'first': {'image': {'url': product.product.images.first().image.url}}},
                    'image_alt': {'first': {'image_alt': product.product.images.first().image_alt}},
                    'name': product.product.name,
                    'category': product.product.category,
                    'price': product.price,
                    'description': product.product.description,
                    'count_reviews': get_count_product_reviews(product.product),
                    'year': year,
                    'rating': product.product.productpurchases.num_purchases,
                }
            )
    return products_list


def get_min_cards(cards, cards_obj):
    """
    :param cards: пустой список
    :param cards_obj: отфильтрованный список товаров по имени
    :return: список товаров с наименьшей ценой
    """
    cards_list = get_seller_products(cards_obj)
    for card in cards_list:
        cards.append(card)
    for card_1 in cards_list:
        for card_2 in cards:
            if card_1['name'] == card_2['name'] and card_1['price'] < card_2['price']:
                cards.pop(cards.index(card_2))
    return cards


def sort_list(cards, sort_by):
    """
    :param cards: список всех товаров
    :param sort_by: имя по которому будет сортировать
    :return: отсортированный список
    """
    if sort_by:
        if type(cards) == Page:
            if sort_by[0] == '-':
                cards.object_list.sort(key=lambda x: x[sort_by[1:]], reverse=True)
            else:
                cards.object_list.sort(key=lambda x: x[sort_by])
        else:
            if sort_by[0] == '-':
                cards.sort(key=lambda x: x[sort_by[1:]], reverse=True)
            else:
                cards.sort(key=lambda x: x[sort_by])
        return cards
    return cards
