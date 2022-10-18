from django.contrib import admin
from .models import TestOrderDetailModel, TestBasketModel, TestSaleModel, TestGoodProfileModel, TestOrderModel,\
    TestUserProfileModel, TestGoodModel


class TestOrderDetailAdmin(admin.ModelAdmin):
    pass


class TestBasketAdmin(admin.ModelAdmin):
    pass


class TestSaleAdmin(admin.ModelAdmin):
    pass


class TestGoodProfileAdmin(admin.ModelAdmin):
    pass


class TestOrderAdmin(admin.ModelAdmin):
    pass


class TestUserProfileAdmin(admin.ModelAdmin):
    pass


class TestGoodAdmin(admin.ModelAdmin):
    pass


admin.site.register(TestOrderDetailModel, TestOrderDetailAdmin)
admin.site.register(TestBasketModel, TestBasketAdmin)
admin.site.register(TestSaleModel, TestSaleAdmin)
admin.site.register(TestGoodProfileModel, TestGoodProfileAdmin)
admin.site.register(TestOrderModel, TestOrderAdmin)
admin.site.register(TestUserProfileModel, TestUserProfileAdmin)
admin.site.register(TestGoodModel, TestGoodAdmin)
