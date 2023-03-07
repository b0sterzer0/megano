from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app_cart.models import AnonimCart
from app_login.models import Profile
from market_app.models import ProductReview, Seller, Product, SellerProduct
from app_settings.utils import get_settings


def get_product_review_list(product, page):
    """
    Функция получает и возвращает список отзывов определенного товара.
    :param product: товар.
    :return: список отзывов определенного товара.
    """

    reviews_list = ProductReview.objects.filter(product=product).select_related('customer').order_by('-date')

    paginator = Paginator(reviews_list, 2)  # По 2 отзыва на каждой странице.
    page = page
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        reviews = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        reviews = paginator.page(paginator.num_pages)
    return reviews


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
    review = ProductReview.objects.create(product=product,
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
    products_obj = []
    for product_form_seller_product in SellerProduct.objects.all():
        if product_form_seller_product.product.name == product_obj.name:
            products_obj.append(product_form_seller_product)
    price_after_discount = products_obj[0]
    for product in products_obj:
        if product.discount:
            return float(product.price) * (1 - product.discount.discount / 100)
    for product in products_obj:
        if product.price < price_after_discount.price:
            price_after_discount = product
    return price_after_discount.price


def get_catalog_product():
    products_list = []
    queryset = Product.objects.all()
    for product_obj in queryset:
        products_list.append(
            {
                'id': product_obj.id,
                'link': product_obj.slug,
                'image': '/static/assets/img/content/home/card.jpg',
                'image_alt': 'card.jpg',
                'name': product_obj.name,
                'category': product_obj.category,
                'price': get_price(product_obj),
                'description': product_obj.description
            }
        )
    return products_list


def get_seller_products(queryset):
    products_list = []
    for product in queryset:
        if product.discount:
            sale = product.discount
            products_list.append(
                {
                    'id': product.id,
                    'seller': product.seller.name,
                    'seller_id': product.seller.id,
                    'link': product.product.slug,
                    'image': '/static/assets/img/content/home/card.jpg',
                    'image_alt': 'card.jpg',
                    'name': product.product.name,
                    'category': product.product.category,
                    'price': float(product.price) * (1 - sale.discount / 100),
                    'price_old': product.price,
                    'sale': sale.discount,
                    'date': sale.start_date,
                    'date_to': sale.end_date,
                    'description': product.product.description
                }
            )
        else:
            products_list.append(
                {
                    'id': product.id,
                    'seller': product.seller.name,
                    'seller_id': product.seller.id,
                    'link': product.product.slug,
                    'image': '/static/assets/img/content/home/card.jpg',
                    'image_alt': 'card.jpg',
                    'name': product.product.name,
                    'category': product.product.category,
                    'price': product.price,
                    'description': product.product.description
                }
            )
    return products_list
