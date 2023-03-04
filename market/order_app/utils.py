from django.core.cache import cache
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate

from app_login.models import Profile


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
