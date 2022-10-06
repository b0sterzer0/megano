from django.shortcuts import render
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    """Главная страница"""
    template_name = 'index.html'

