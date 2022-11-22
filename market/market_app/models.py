from django.contrib.auth.models import User
from django.db import models
from catalog_categories.models import Category


class Banner(models.Model):
    """ Модель рекламного баннера на главной странице сайта """
    title = models.CharField(max_length=50, verbose_name='заголовок')
    # Цены в рублях (без копеек)
    price = models.IntegerField(verbose_name='цена')
    image = models.ImageField(upload_to='images/banners', verbose_name='изображение')
    image_alt = models.CharField(max_length=100, verbose_name='подсказка')
    link = models.CharField(max_length=300, verbose_name='url')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'баннер'
        verbose_name_plural = 'баннеры'


class Seller(models.Model):
    """Заглушка модели продавца"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Discount(models.Model):
    """Модель скидки для товаров"""
    discount = models.IntegerField()

    class Meta:
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    category = models.ForeignKey("catalog_categories.Category", on_delete=models.CASCADE, related_name='products',
                                 verbose_name='Категория')
    seller = models.ManyToManyField(Seller, through='SellerProduct', related_name='products',
                                    verbose_name='Продавец')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    """Модель фотографий к товарам"""
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/products/%Y/%m/%d', verbose_name='Картинка')
    image_alt = models.CharField(max_length=100, default='Фото к отзыву', verbose_name='подсказка')


class ProductDiscount(models.Model):
    """Промежуточная модель между моделями товара и скидки"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, verbose_name='Скидка')

    class Meta:
        verbose_name = 'Товар-скидка'
        verbose_name_plural = 'Товар-скидка'


class SellerProduct(models.Model):
    """Промежуточная модель между моделями товара и продавца"""
    product = models.ForeignKey("Product", on_delete=models.CASCADE, verbose_name='Товар')
    seller = models.ForeignKey("Seller", on_delete=models.CASCADE, verbose_name='Продавец')
    qty = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f'{self.product.name} - {self.seller.id}'

    class Meta:
        verbose_name = 'Товар-продавец'
        verbose_name_plural = 'Товар-продавец'


class ProductReview(models.Model):
    """Модель отзывов к товарам определенных продавцов"""
    product = models.ForeignKey("Product", on_delete=models.CASCADE, verbose_name='Отзывы товаров',
                                related_name='reviews'
                                )
    # Изменить пользователя после создания app_user
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель', related_name='customer')
    description = models.TextField(max_length=2000, verbose_name='Описание')

    def description_short(self):
        """
        Функция возвращает описание, если его длина меньше 15 символов, иначе возвращает
        срез первых 15 символов с многоточием.
        :return: обрезанное описание.
        """
        if len(self.description) > 15:
            return self.description[:15] + '...'
        return self.description

    def __str__(self):
        return f'Запись: {self.description_short()}, Пользователь: {self.customer}'

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарий'


class ProductReviewImage(models.Model):
    """Модель фотографий к отзывам"""
    review = models.ForeignKey("ProductReview", on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/product_reviews/%Y/%m/%d', verbose_name='Картинка')
    image_alt = models.CharField(max_length=100, default='Фото к отзыву', verbose_name='подсказка')
