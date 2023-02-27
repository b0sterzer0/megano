from django.contrib import admin

from .models import TestBasketModel


class TestBasketAdmin(admin.ModelAdmin):
    pass


admin.site.register(TestBasketModel, TestBasketAdmin)
