from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseBadRequest

from requests import get as req_get
from typing import Union

from .models import TestBasketModel
from market_app.models import SellerProduct
from api_for_payment_app.models import PaymentStatusModel


def get_total_price(user_from_req) -> int:
    """
    Функция вычисляет общую цену товаров в корзине
    """
    products_in_basket_list = TestBasketModel.objects.filter(user=user_from_req)

    total_price = 0
    for product_in_basket in products_in_basket_list:
        try:
            product_price = SellerProduct.objects.get(product=product_in_basket.product).price
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Ошибка: цена для товара не найдена')
        total_price += product_price
    return int(total_price)


def get_dict_with_payment_status(base_url: str, card_number: str, total_price: int) -> dict:
    """
    Функция получает от API, симулирующего работу банка, статус оплаты
    """
    data_from_api = req_get(url=f'{base_url}/APIPayment/{card_number}/{total_price}')

    if data_from_api.status_code != 200:
        status = PaymentStatusModel.objects.get(status_code='S204')
        status = {'status': {'status_code': status.status_code,
                             'status_description': status.status_description}}
        return status

    status = data_from_api.json()
    return status


def post_method_for_payment_views(request) -> dict:
    """
    В этой функции реализован POST метод для представлений PayMyCardView и PaySomeoneCardView
    """
    base_url = 'http://127.0.0.1:8000'
    card_number = request.POST.get('card_number')
    if card_number:
        total_price = get_total_price(request.user)
        payment_status = get_dict_with_payment_status(base_url, card_number, total_price)
        return payment_status
