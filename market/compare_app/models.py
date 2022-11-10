from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class TestCategory(models.Model):
    name = models.CharField(max_length=30, verbose_name='название категории')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class TestProduct(models.Model):
    name = models.CharField(max_length=30, verbose_name='имя товара')
    paths_to_good_images = ArrayField(models.CharField(max_length=100))
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, null=True, default=None,
                                 verbose_name='категория')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class TestSpecification(models.Model):
    code = models.CharField(max_length=30, verbose_name='код спецификации')
    name = models.CharField(max_length=30, verbose_name='название спецификации')
    uom = models.CharField(max_length=30, verbose_name='хз что это')

    class Meta:
        verbose_name = 'спецификация'
        verbose_name_plural = 'спецификации'

    def __str__(self):
        return self.name


class TestSpecificationValue(models.Model):
    specification = models.ForeignKey(TestSpecification, on_delete=models.CASCADE, default=None, null=True,
                                         verbose_name='спецификация')
    product = models.ForeignKey(TestProduct, on_delete=models.CASCADE, null=True, default=None, verbose_name='товар')
    value = models.CharField(max_length=30, verbose_name='значение спецификации')

    class Meta:
        verbose_name = 'спецификация товара'
        verbose_name_plural = 'спецификации товара'

    def __str__(self):
        return self.specification.name
