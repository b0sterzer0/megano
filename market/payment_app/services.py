import json

from requests import get as req_get

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from api_for_payment_app.models import PaymentStatusModel
from order_app.models import OrderModel


def get_total_price(order_id) -> int:
    """
    Функция находит общую цену заказа
    """

    try:
        order_object = OrderModel.objects.get(id=order_id)
        order_data = json.loads(order_object.json_order_data)
        total_price = order_data['t_price']
    except ObjectDoesNotExist:
        return HttpResponse('Ошибка: заказ не найден')
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


def change_payment_status_in_order(order_id):
    """
    Функция обновляет статус оплаты в заказе на 'Оплачено'
    """
    order = OrderModel.objects.get(id=order_id)
    deserialized_data_dict = json.loads(order.json_order_data)
    deserialized_data_dict['order_dict']['payment_status'] = 'Оплачено'
    serialized_data_dict = json.dumps(deserialized_data_dict)
    order.json_order_data = serialized_data_dict
    order.save()


def post_method_for_payment_views(request, order_id) -> dict:
    """
    В этой функции реализован POST метод для представлений PayMyCardView и PaySomeoneCardView
    """
    base_url = 'http://127.0.0.1:8000'
    card_number = request.POST.get('card_number')
    if card_number:
        total_price = get_total_price(order_id)
        payment_status = get_dict_with_payment_status(base_url, card_number, total_price)
        if payment_status['status']['status_code'] == 'S200':
            change_payment_status_in_order(order_id)
        return payment_status
