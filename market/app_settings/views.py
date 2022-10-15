from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from .forms import SettingsForm
from .models import SiteSettings


class SettingsView(View):
    """Класс-представление страницы настроек"""
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def get(self, request):
        """
        Функция обрабатывающая GET запрос, возвращает страницу настроек с формой
        настроек.
        """
        settings = SiteSettings.objects.first()
        settings_form = SettingsForm(instance=settings)
        return render(request, 'settings.html', context={'settings_forms': settings_form})

    def post(self, request):
        """
        Функция обрабатывающая POST запрос со страницы настроек, сохраняет данные формы
        настроек или ловит нажатие одной из кнопок сброса кэша.
        """
        # После добавления кэша разделов, удалить принты!!!
        settings = SiteSettings.objects.first()
        settings_form = SettingsForm(request.POST, instance=settings)
        if 'section1' in request.POST:
            print('раздел 1 сброшен')
        elif 'section2' in request.POST:
            print('раздел 2 сброшен')
        elif 'section3' in request.POST:
            print('раздел 3 сброшен')
        elif 'all' in request.POST:
            cache.clear()
            print('Весь кэш сброшен')

        if settings_form.is_valid():
            settings.save()
        return HttpResponseRedirect(reverse('settings'))
