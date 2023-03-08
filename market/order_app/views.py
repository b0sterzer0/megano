from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from django.core.cache import cache

from app_login.models import Profile
from order_app.utils import add_data_in_order_cache, if_user_is_not_authenticate, get_products_from_cart_for_anon_user,\
get_products_from_cart_for_auth_user


class OrderStepOneView(View):
    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                user_email = User.objects.get(id=request.user.id).email
                context = {'full_name': profile.full_name,
                           'phone': profile.phone,
                           'email': user_email}

            except ObjectDoesNotExist:
                return HttpResponse('Не удалось получить данные пользователя')

        return render(request, 'order/order_step_1.html', context=context)

    def post(self, request):
        data_dict = {'full_name': request.POST.get('name'),
                     'phone': request.POST.get('phone'),
                     'mail': request.POST.get('mail')}
        add_data_in_order_cache(**data_dict)
        if not request.user.is_authenticated:
            data_dict['password'] = request.POST.get('password')
            user = if_user_is_not_authenticate(request, **data_dict)
            if user:
                return HttpResponseRedirect(reverse('login'))

        return HttpResponseRedirect(reverse('order_step_2'))


class OrderStepTwoView(View):
    def get(self, request):
        context = {}
        order_dict = cache.get('order') or {}
        if 'delivery' in order_dict.keys():
            context = {'delivery': order_dict['delivery'],
                       'city': order_dict['city'],
                       'address': order_dict['address']}
        return render(request, 'order/order_step_2.html', context)

    def post(self, response):
        data_dict = {'delivery': response.POST.get('delivery'),
                     'city': response.POST.get('city'),
                     'address': response.POST.get('address')}
        add_data_in_order_cache(**data_dict)

        return HttpResponseRedirect(reverse('order_step_3'))


class OrderStepThreeView(View):
    def get(self, request):
        context = {}
        order_dict = cache.get('order') or {}
        if 'pay' in order_dict.keys():
            context = {'pay': order_dict['pay']}
        return render(request, 'order/order_step_3.html', context)

    def post(self, response):
        add_data_in_order_cache(**{'pay': response.POST.get('pay')})

        return HttpResponseRedirect(reverse('order_step_4'))


class OrderStepFourView(View):
    def get(self, request):
        if request.user.is_authenticated:
            total_price, products = get_products_from_cart_for_auth_user(request)
        else:
            total_price, products = get_products_from_cart_for_anon_user(request)

        order_dict = cache.get('order')
        print(f'!!!! {order_dict} !!!!!!')

        return render(request, 'order/order_step_4.html', context={'t_price': total_price,
                                                                   'products_list': products,
                                                                   'order_dict': order_dict})

    def post(self, response):
        return HttpResponse('OK')