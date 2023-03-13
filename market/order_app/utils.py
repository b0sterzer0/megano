from django.core.cache import cache
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import HttpResponseRedirect

from app_login.models import Profile
from app_cart.models import AnonimCart, AuthShoppingCart
from market_app.models import Product, ProductImage, SellerProduct
from app_settings.models import SiteSettings


def add_data_in_order_cache(**kwargs):
    order_dict = cache.get('order') or {}
    for key, value in kwargs.items():
        order_dict[key] = value
    cache.set('order', order_dict)


def delete_data_from_order_cache(*args):
    order_dict = cache.get('order') or {}
    for key in args:
        order_dict.pop(key)
    cache.set('order', order_dict)


def create_user_from_order_data(email, password):
    user = User.objects.create_user(username=email, email=email)
    user.set_password(password)
    group = Group.objects.get(name='customer')
    user.groups.add(group)
    user.save()
    return user


def if_user_is_not_authenticate(request, **user_data):
    users = User.objects.filter(username=user_data['mail'])
    if not users:
        users = User.objects.filter(email=user_data['mail'])
    if users:
        return users.first()
    else:
        user = create_user_from_order_data(email=user_data['mail'], password=user_data['password'])
        Profile.objects.create(user=user, full_name=user_data['full_name'], phone=user_data['phone'], avatar='none')
        user = authenticate(username=user_data['mail'], password=user_data['password'])
        if user:
            login(request, user)
            return user


def is_one_seller(products_id):
    sellers_set = set()
    for product_id in products_id:
        seller = SellerProduct.objects.select_related('product', 'seller').get(product=product_id).seller
        sellers_set.add(seller)
    if len(sellers_set) == 1:
        return True
    else:
        return False


def get_data_from_cart_for_anon_user(request):
    cart = AnonimCart(request)
    cart_dict = cart.get_cart()
    total_price = cart.get_total_price()
    products = []
    products_id = []
    for product_id in cart_dict.keys():
        product_dict = {}
        try:
            product = Product.objects.select_related('category').get(id=product_id)
            product_dict['image'] = ProductImage.objects.get(product=product.id).image
            product_dict['category'] = product.category.title
            product_dict['description'] = product.description
            product_dict['qty'] = cart_dict[product_id]['count']
            product_dict['price'] = float(cart_dict[product_id]['price']) * float(product_dict['qty'])
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('del_product_cart'), {'product_id': product_id})
        products.append(product_dict)
        products_id.append(product_id)
    one_seller = is_one_seller(products_id=products_id)

    return total_price, products, one_seller


def get_data_from_cart_for_auth_user(request):
    products_in_cart = AuthShoppingCart.objects.select_related('products').filter(user=request.user)
    total_price = 0
    products = []
    products_id = []
    for product in products_in_cart:
        product_dict = {}
        try:
            product_dict['image'] = ProductImage.objects.get(product=product.products.id).image
            product_dict['category'] = product.products.category.title
            product_dict['description'] = product.products.description
            product_dict['qty'] = product.count
            product_dict['price'] = float(product.price) * float(product_dict['qty'])
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('del_product_cart'), {'product_id': product.products.id})
        products.append(product_dict)
        total_price += product_dict['price']
        products_id.append(product.products.id)

    one_seller = is_one_seller(products_id)

    return total_price, products, one_seller


def calculate_delivery_cost(order_data, one_seller):
    settings = SiteSettings.objects.all().first()
    delivery_cost = 0
    if order_data['order_dict']['delivery'] == 'express':
        delivery_cost = int(settings.express_delivery_cost)
    elif order_data['order_dict']['delivery'] == 'ordinary':
        if order_data['t_price'] < settings.min_amount_for_free_delivery or not one_seller:
            delivery_cost = int(settings.ordinary_delivery_cost)

    return delivery_cost


def check_cache(order_dict):
    if order_dict:
        if {'full_name', 'delivery', 'pay'}.issubset(set(order_dict.keys())):
            return None
    return HttpResponseRedirect(reverse('order_step_1'))
