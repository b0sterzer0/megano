from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


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
