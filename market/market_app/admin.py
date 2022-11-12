from django.contrib import admin
from .models import Banner, Product, SellerProduct, Category, Seller, Discount, ProductDiscount


@admin.register(Banner)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'image_alt']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(SellerProduct)
class SellerProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'seller', 'qty', 'price']
    list_filter = ['product', 'seller']
    search_fields = ['product', 'seller']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    pass


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['discount']


@admin.register(ProductDiscount)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['product', 'discount']
