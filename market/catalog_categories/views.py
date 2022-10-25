from django.views.generic import ListView
from .models import Category


class CategoryListView(ListView):
    """
    Представление для категорий товаров у которых activity = True.
    """

    template_name = "category/category.html"
    model = Category

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(activity=True).order_by('id')
