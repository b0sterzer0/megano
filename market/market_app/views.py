from django.shortcuts import render
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    """Главная страница"""
    template_name = 'index.html'


class AboutView(TemplateView):
    """About"""
    template_name = 'about.html'
    extra_context = {'middle_title_left': 'About Megano', 'middle_title_right': 'About Us'}


class AccountView(TemplateView):
    """Account"""
    template_name = 'account.html'
    extra_context = {'middle_title_left': 'Личный кабинет', 'middle_title_right': 'Личный кабинет'}


class CartView(TemplateView):
    """Cart"""
    template_name = 'cart.html'
    extra_context = {'middle_title_left': 'Корзина', 'middle_title_right': 'Корзина'}
