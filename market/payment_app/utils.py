import json

from requests import get

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from api_for_payment_app.models import PaymentStatusModel
from order_app.models import OrderModel
from market_app.models import Product, ProductPurchases


def get_total_price(order_id: str) -> str:
    """
    Функция находит общую цену заказа
    """

    try:
        order_object = OrderModel.objects.get(id=order_id)
        order_data = json.loads(order_object.json_order_data)
        total_price = order_data['t_price']
        if not order_data['products_list']:
            total_price = None
    except ObjectDoesNotExist:
        return HttpResponse('Ошибка: заказ не найден')
    return total_price


def create_payment_status_dict(s_code: str) -> dict:
    """
    Функция создает словарь статуса оплаты заказа по данным, получаемым из БД
    """
    status = PaymentStatusModel.objects.get(status_code=s_code)
    status = {'status': {'status_code': status.status_code,
                         'status_description': status.status_description}}
    return status


def get_dict_with_payment_status(base_url: str, card_number: str, total_price: int) -> dict:
    """
    Функция получает от API, симулирующего работу банка, статус оплаты
    """
    data_from_api = get(url=f'{base_url}/APIPayment/{card_number}/{total_price}/')

    if data_from_api.status_code != 200:
        return create_payment_status_dict('S204')

    status = data_from_api.json()
    return status


def change_payment_status_in_order(order_id: str) -> None:
    """
    Функция обновляет статус оплаты в заказе на 'Оплачено'
    """
    order = OrderModel.objects.get(id=order_id)
    deserialized_data_dict = json.loads(order.json_order_data)
    deserialized_data_dict['order_dict']['payment_status'] = 'Оплачено'
    serialized_data_dict = json.dumps(deserialized_data_dict)
    order.json_order_data = serialized_data_dict
    order.save()


def increase_product_purchases(order_id: str) -> None:
    """
    Функция увеличивает кол-во единиц проданного товара в таблице ProductPurchases
    """
    order = OrderModel.objects.get(id=order_id)
    deserialized_data_dict = json.loads(order.json_order_data)
    for product_from_order in deserialized_data_dict['products_list']:
        product = Product.objects.get(id=product_from_order['product_id'])
        product_purchases = ProductPurchases.objects.filter(product=product)
        if product_purchases:
            product_purchases = product_purchases.first()
            product_purchases.num_purchases += (1 * product_from_order['qty'])
            product_purchases.save()
        else:
            ProductPurchases.objects.create(product=product, num_purchases=1)


def post_method_for_payment_views(request, order_id: str) -> dict:
    """
    В этой функции реализован POST метод для представлений PayMyCardView и PaySomeoneCardView
    """
    base_url = 'http://127.0.0.1:8000'
    card_number = request.POST.get('card_number')
    if card_number:
        total_price = get_total_price(order_id)
        if total_price is None:
            return create_payment_status_dict('S000')
        payment_status = get_dict_with_payment_status(base_url, card_number, int(total_price))
        if payment_status['status']['status_code'] == 'S200':
            change_payment_status_in_order(order_id)
            increase_product_purchases(order_id)
        return payment_status
