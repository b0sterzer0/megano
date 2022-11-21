from django.contrib import admin

from market_app.models import Banner, Product, ProductImage, ProductReview, ProductReviewImage, Seller, \
    SellerProduct


@admin.register(Banner)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'image_alt']


class ProductImageInline(admin.TabularInline):
    """Класс для создания inline в модели товара в админке"""
    model = ProductImage
    extra = 1
    max_num = 10


class ProductReviewImageInline(admin.TabularInline):
    """Класс для создания inline в модели отзывов к товару в админке"""
    model = ProductReviewImage
    extra = 1
    max_num = 10


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Класс для работы с моделью товаров в админке"""
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]


@admin.register(SellerProduct)
class SellerProductAdmin(admin.ModelAdmin):
    """Класс для работы с моделью товаров у продавцов в админке"""
    list_display = ['product', 'seller', 'qty', 'price']
    list_filter = ['product', 'seller']
    search_fields = ['product', 'seller']


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    """Класс для работы с моделью продавцов в админке"""
    list_display = ['name']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """Класс для работы с моделью отзывов к товарам в админке"""
    list_display = ['product', 'customer', 'description_short']
    search_fields = ['product', 'customer']
    inlines = [ProductReviewImageInline]
