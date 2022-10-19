from django.contrib import admin

from .models import Banner


@admin.register(Banner)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'image_alt']

