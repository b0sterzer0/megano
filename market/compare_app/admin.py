from django.contrib import admin
from .models import TestProduct, TestSpecification, TestCategory, TestSpecificationValue


class TestProductAdmin(admin.ModelAdmin):
    pass


class TestCategoryAdmin(admin.ModelAdmin):
    pass


class TestSpecificationAdmin(admin.ModelAdmin):
    pass


class TestSpecificationValueAdmin(admin.ModelAdmin):
    pass


admin.site.register(TestProduct, TestProductAdmin)
admin.site.register(TestSpecification, TestSpecificationAdmin)
admin.site.register(TestSpecificationValue, TestSpecificationValueAdmin)
admin.site.register(TestCategory, TestCategoryAdmin)
