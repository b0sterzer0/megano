from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import RegisterForm, AuthForm
from .models import Profile
from .utils import transfer_to_auth_cart
from market_app.models import Category
from django.views import View
from django.contrib.auth.views import (LogoutView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)


categories = Category.objects.all()


class LoginUserView(View):

    """Аунтификация  пользователя"""

    def get(self, request):

        auth_form = AuthForm()
        return render(request, 'login.html', context={'auth_form': auth_form,
                                                      'middle_title_left': 'Войти на сайт',
                                                      'middle_title_right': 'Войти на сайт'})

    def post(self, request):

        auth_form = AuthForm(request.POST)

        if auth_form.is_valid():

            username = auth_form.cleaned_data['username']
            password = auth_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            transfer_to_auth_cart(request, user)
            login(request, user)
            return HttpResponseRedirect('/')

        return render(request, 'login.html', context={'auth_form': auth_form,
                                                      'middle_title_left': 'Войти на сайт',
                                                      'middle_title_right': 'Войти на сайт'})


class LogoutUserView(LogoutView):
    """
    Завершение сессии пользователя
    """
    next_page = '/'


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            transfer_to_auth_cart(request, user)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form,
                                                 'categories': categories,
                                                 'middle_title_left': 'зарегистрироваться',
                                                 'middle_title_right': 'зарегистрироваться'})


class UserResetPasswordView(PasswordResetView):
    template_name = 'registration/password_reset.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['middle_title_left'] = 'Восстановление пароля'
        context['middle_title_right'] = 'Восстановление пароля'
        return context


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['middle_title_left'] = 'Восстановление пароля'
        context['middle_title_right'] = 'Восстановление пароля'
        return context


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['middle_title_left'] = 'Восстановление пароля'
        context['middle_title_right'] = 'Восстановление пароля'
        return context


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['middle_title_left'] = 'Восстановление пароля'
        context['middle_title_right'] = 'Восстановление пароля'
        return context
