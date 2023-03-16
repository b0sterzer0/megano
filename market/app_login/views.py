from decimal import Decimal
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from app_cart.models import AnonimCart, AuthShoppingCart
from .forms import RegisterForm
from .models import Profile
from market_app.models import Category
from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)


categories = Category.objects.all()


class LoginUserView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['middle_title_left'] = 'Войти на сайт'
        context['middle_title_right'] = 'Войти на сайт'
        return context


class LogoutUserView(LogoutView):
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
            anonim_cart = AnonimCart(request)
            if len(anonim_cart.get_cart()) != 0:
                cart = anonim_cart.get_cart()
                for item in cart.keys():
                    product = int(item)
                    AuthShoppingCart.objects.create(
                        user_id=user.id,
                        products_id=product,
                        count=cart[item]['count'],
                        price=Decimal(cart[item]['price'])
                    )
                cart.clear()
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
