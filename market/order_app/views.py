from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from django.core.cache import cache

from app_login.models import Profile
from order_app.utils import add_data_in_order_cache, if_user_is_not_authenticate
from app_cart.models import AnonimCart
from market_app.models import Product, ProductImage


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
        cart = AnonimCart(request)
        cart_dict = cart.get_cart()
        total_price = 0
        products = []
        for product_id in cart_dict.keys():
            product_dict = {}
            try:
                product = Product.objects.select_related('category').get(id=product_id)
                product_dict['image'] = ProductImage.objects.get(product).image
                product_dict['category'] = product.category.title
                product_dict['description'] = product.description
                product_dict['price'] = cart_dict[product_id]['price']
                product_dict['qty'] = cart_dict[product_id]['count']
            except ObjectDoesNotExist:
                return HttpResponseRedirect(reverse('del_product_cart'), {'product_id': product_id})
            total_price += product_dict['price']
            products.append(product_dict)

        return render(request, 'order/order_step_4.html')

    def post(self, response):
        return HttpResponse('OK')