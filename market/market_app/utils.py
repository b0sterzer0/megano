from market_app.models import ProductReview, ProductReviewImage


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
