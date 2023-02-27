from django.shortcuts import render
from django.views import View

from .services import post_method_for_payment_views


class PayMyCardView(View):
    """
    Представления для вывода страницы payment.html и получения информации с нее
    """
    def get(self, request) -> render:
        return render(request, 'payment.html', context={'middle_title_left': 'Оплата',
                                                        'middle_title_right': 'Оплата'})

    def post(self, request) -> render:
        payment_status = post_method_for_payment_views(request)
        return render(request, 'progressPayment.html',
                      context={'message_status': payment_status['status']['status_description'],
                               'status_code': payment_status['status']['status_code'],
                               'middle_title_left': 'Оплата',
                               'middle_title_right': 'Оплата'})


class PaySomeoneCardView(View):
    """
    Представления для вывода страницы paymentsomeone.html и получения информации с нее
    """
    def get(self, request) -> render:
        return render(request, 'paymentsomeone.html', context={'middle_title_left': 'Оплата',
                                                               'middle_title_right': 'Оплата'})

    def post(self, request) -> render:
        payment_status = post_method_for_payment_views(request)
        return render(request, 'progressPayment.html',
                      context={'message_status': payment_status['status']['status_description'],
                               'status_code': payment_status['status']['status_code'],
                               'middle_title_left': 'Оплата',
                               'middle_title_right': 'Оплата'})
