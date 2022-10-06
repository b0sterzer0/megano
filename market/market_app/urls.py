from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('account/', views.AccountView.as_view(), name='account'),
]
