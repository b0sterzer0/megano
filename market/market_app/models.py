from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


class Banner(models.Model):
    """ Модель рекламного баннера на главной странице сайта """
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    # Цены в рублях (без копеек)
    price = models.IntegerField(verbose_name='Цена')
    image = models.ImageField(upload_to='images/banners', verbose_name='Изображение')
    image_alt = models.CharField(max_length=100, verbose_name='Подсказка')
    link = models.CharField(max_length=300, verbose_name='url')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'


class Seller(models.Model):
    """Модель продавца"""

    profile = models.ForeignKey("app_login.Profile", on_delete=models.CASCADE,
                                related_name='sellers', verbose_name=_('профиль')
                                )
    description = models.TextField(max_length=2000, blank=True, verbose_name=_('описание'))
    name = models.CharField(max_length=200, verbose_name=_('название магазина'))
    logo = models.ImageField(upload_to='seller_files/')

    class Meta:
        verbose_name = _('продавец')
        verbose_name_plural = _('продавцы')

    def __str__(self):
        return self.profile.user.username


class Category(MPTTModel):
    """
    Класс модели -> Category
    title - название категории;
    slug - повторение имени;
    parent - родительская категория;
    activity - флаг активности новости;
    """

    title = models.CharField(max_length=50, unique=True, verbose_name='Название')
    slug = models.SlugField()
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    activity = models.BooleanField(default=False, blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Discount(models.Model):
    """Модель скидки для товаров"""
    discount = models.IntegerField()

    class Meta:
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=255, db_index=True, verbose_name=_('название'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',
                                 verbose_name=_('категория'))
    seller = models.ManyToManyField(Seller, through='SellerProduct', related_name='products',
                                    verbose_name=_('продавец'))
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(max_length=2000, default='description', verbose_name=_('описание'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('товар')
        verbose_name_plural = _('товары')


class ProductImage(models.Model):
    """Модель фотографий к товарам"""
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/products/%Y/%m/%d', verbose_name=_('картинка'))
    image_alt = models.CharField(max_length=100, default='Фото к товару', verbose_name=_('подсказка'))


class ProductDiscount(models.Model):
    """Промежуточная модель между моделями товара и скидки"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, verbose_name='Скидка')

    class Meta:
        verbose_name = 'Товар-скидка'
        verbose_name_plural = 'Товар-скидка'


class SellerProduct(models.Model):
    """Промежуточная модель между моделями товара и продавца"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('товар'), related_name='sellers')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name=_('продавец'), related_name='sellers')
    qty = models.PositiveIntegerField(verbose_name=_('количество'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('цена'))

    def __str__(self):
        return f'{self.product.name} - {self.seller.name}'

    class Meta:
        verbose_name = _('товар-продавец')
        verbose_name_plural = _('товар-продавец')


class HistoryView(models.Model):
    """ История просмотров пользователя """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    view_time = models.DateTimeField(auto_now=True, auto_created=True, verbose_name='Время просмотра')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'История просмотров'
        verbose_name_plural = 'История просмотров'
        ordering = ['view_time']


class ProductReview(models.Model):
    """Модель отзывов к товарам определенных продавцов"""
    product = models.ForeignKey("Product", on_delete=models.CASCADE, verbose_name=_('товар'),
                                related_name='reviews'
                                )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('покупатель'), related_name='reviews')
    description = models.TextField(max_length=2000, verbose_name=_('описание'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('дата'))

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
        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')


class ProductReviewImage(models.Model):
    """Модель фотографий к отзывам"""
    review = models.ForeignKey("ProductReview", on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/product_reviews/%Y/%m/%d', verbose_name=_('картинка'))
    image_alt = models.CharField(max_length=100, default='Фото к отзыву', verbose_name=_('подсказка'))
