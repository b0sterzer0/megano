from django.db import models


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
    pass


class Category(models.Model):
    """Заглушка модели категорий"""
    pass


class Discount(models.Model):
    discount = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',
                                 verbose_name='Категория')
    seller = models.ManyToManyField(Seller, through='SellerProduct', related_name='products',
                                    verbose_name='Продавец')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='products',
                                 verbose_name='Скидка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class SellerProduct(models.Model):
    """Промежуточная модель между моделями товара и продавца"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name='Продавец')
    qty = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f'{self.product.name} - {self.seller.id}'

    class Meta:
        verbose_name = 'Товар-продавец'
        verbose_name_plural = 'Товар-продавец'
