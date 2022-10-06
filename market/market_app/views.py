from django.shortcuts import render
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    """Главная страница"""
    template_name = 'index.html'


class AboutView(TemplateView):
    """About"""
    template_name = 'about.html'
    extra_context = {'middle_title_left': 'About Megano', 'middle_title_right': 'About Us'}

