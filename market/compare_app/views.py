from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.cache import cache

from market_app.models import Product, CharacteristicsGroup, Characteristic, CharacteristicValue, ProductImage


def add_good_for_compare_view(request, product_id: int) -> HttpResponseRedirect or HttpResponse:
    """
    Это представление реализует добавление товара в список для сравнения, хранящийся к кэше
    """
    if request.method == "GET":
        try:
            product = Product.objects.select_related('category').get(id=product_id)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Продукт не найден')

        compare_object = cache.get('compare_object')
        if compare_object:
            if not compare_object['category_for_compare'] == product.category:
                return render(request, 'comparison.html', context={'products_for_compare_dict': None,
                                                                   'isFalseCategory': True})

            if len(compare_object['products_list']) < 2:
                compare_object['products_list'].append(product.id)
                cache.set('compare_object', compare_object)
            else:
                compare_object['products_list'].pop(0)
                compare_object['products_list'].append(product.id)
                cache.set('compare_object', compare_object)
        else:
            cache.set('compare_object',
                      {
                          'category_for_compare': product.category,
                          'products_list': [product_id]
                      }
                      )
        return HttpResponseRedirect('/comparison/')


def remove_good_for_compare_view(request, product_id: int) -> HttpResponseRedirect or HttpResponse:
    """
    Данное представление удаляет товар из списка товаров для сравнения в кэше по переданному product_id
    """
    compare_object = cache.get('compare_object')

    if compare_object:
        try:
            compare_object['products_list'].remove(product_id)
            cache.set('compare_object', compare_object)
            if len(cache.get('compare_object')['products_list']) < 1:
                cache.delete('compare_object')
            return HttpResponseRedirect('/comparison/')
        except ValueError:
            return HttpResponseBadRequest('Ошибка: не удалось удалить товар из списка товаров для сравнения')
    else:
        return HttpResponseBadRequest('Ошибка: данной записи в кэше не существует')


def get_products_for_compare(compare_object: dict) -> dict:
    """
    Данная функция собирает все необходимые данные в словарь, который впоследствии будет передан в шаблон.

    Структура словаря:
    { Название товара :
        {
            'image_path' (str) - путь до фото товара,
            'product_id' (str) - id товара,
            'characteristics' (dict) :
                {
                    Группа характеристик :
                    [
                        [
                            Название характеристики,
                            Значение характеристики
                        ],
                        ....
                    ],
                    ....
                }
        }
    }
    """

    products_for_compare_dict = dict()
    for product_id in compare_object['products_list']:
        try:
            product = Product.objects.get(id=product_id)
            image_path = ProductImage.objects.get(product=product).image
            products_for_compare_dict[product.name] = {'image_path': image_path,
                                                       'product_id': product.id,
                                                       'characteristics': dict()}

            characteristics = CharacteristicValue.objects.select_related('characteristic').filter(product=product)
            if not characteristics:
                raise ObjectDoesNotExist

            existing_groups = list()
            for characteristic in characteristics:
                characteristic_list = [characteristic.characteristic.characteristic_name, characteristic.value]
                for characteristic_group in characteristic.characteristic.group.all():
                    group_name = characteristic_group.group_name
                    if group_name in existing_groups:
                        products_for_compare_dict[product.name]['characteristics'][group_name].append(characteristic_list)
                    else:
                        products_for_compare_dict[product.name]['characteristics'][group_name] = [characteristic_list]
                        existing_groups.append(group_name)

        except ObjectDoesNotExist:
            return HttpResponse('Ошибка: не удалось сформировать словарь для сравнения товаров')

    return products_for_compare_dict

# TODO функция пока закомментирована. Определиться, нужен ли вывод кол-ва добавленных товаров для сравнения
# def get_number_goods_for_compare() -> int:
#     """
#     Данная функция реализует получение кол-ва товаров, добавленных в список для сравнения
#     """
#     compare_object = cache.get('compare_object')
#     if compare_object is None:
#         return 0
#     else:
#         return len(compare_object['products_list'])


def get_products_list_for_compare_view(request) -> render:
    """
    Представление для вывода данных о товарах, добавленных в список для сравнения
    """
    compare_object = cache.get('compare_object')
    if compare_object is None:
        products_for_compare_dict = None
    else:
        products_for_compare_dict = get_products_for_compare(compare_object)
    return render(request, 'comparison.html', context={'products_for_compare_dict': products_for_compare_dict,
                                                       'isFalseCategory': False})
