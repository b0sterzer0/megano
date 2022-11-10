from django.shortcuts import render
from .models import TestProduct, TestSpecificationValue
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from django.core.cache import cache


def add_good_for_compare_view(request, product_id: int) -> HttpResponseRedirect or HttpResponse:
    """
    Это представление реализует добавление товара в список для сравнения.
    Находим нужный товар в TestProduct используя переданный product_id. После этого
    получаем из кэша объект compare_object. Если его не существует - создаем.
    Если существует, то проверяем категорию товаров и кол-во уже добавленных товаров в списке.
    Если не та категория - то возвращаем сообщение об ошибке.
    Если больше 4 и одинаковая категория, то удаляем первый и добавляем в конец новый.
    Если меньше 4 и одинаковая категория, то просто добавляем в конец новый товар.

    :param request:
    :type product_id: int
    :param product_id: id добавляемого товара
    """
    if request.method == "GET":
        try:
            product = TestProduct.objects.select_related('category').get(id=product_id)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Couldnt find product')

        compare_object = cache.get('compare_object')

        if compare_object:

            if not compare_object['category_for_compare'] == product.category:
                return HttpResponseBadRequest('Another category')

            if len(compare_object['products_list']) < 4:
                compare_object['products_list'].append(product.id)
                cache.set('compare_object', compare_object)
            else:
                compare_object['products_list'] = compare_object['products_list'][1::]
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
    Данное представление удаляет товар из списка товаров для сравнения по переданному product_id

    :param request:
    :type product_id: int
    :param product_id: id товара, который нужно удалить из списка товаров для сравнения
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
    products (list) - список объектов модели TestProduct
    ratings (list) - список словарей. Каждый словарь имеет 2 ключа:
    1) название товара (product_name)
    2) значение спецификации, т.е. число, отражающее рейтинг товара от 0 до 5 (specification_value)
    specifications_for_compare (dict) - словарь списков, где ключ - это название конкретной спецификации,
    а значение - список, состоящий из словарей, содержащих два ключа:
    1) название товара (product_name)
    2) значение спецификации (specification_value)

    :type compare_object: dict
    :param compare_object: словарь, полученный из кэша в get_goods_list_for_compare_view()
    """
    products_for_compare = {'products': list(), 'ratings': list(), 'specifications_for_compare': dict()}
    for product_id in compare_object['products_list']:
        try:
            # Находим продукт и добавляем его в список к остальным
            product = TestProduct.objects.get(id=product_id)
            products_for_compare['products'].append(product)
            specification_values = TestSpecificationValue.objects.select_related('specification').filter(product=product)
            for spec in specification_values:

                # Исключаем рейтинг из общего словаря иных спецификаций
                if not spec.specification.name == 'Рейтинг' and not spec.specification.name == 'рейтинг':
                    spec_for_compare_list = products_for_compare['specifications_for_compare'].keys()

                    # Проверяем находится ли уже данная спецификация в списке. Если нет - создаем, если находится -
                    # то добавляем значения к уже имеющимся
                    spec_dict = {
                                    'product_name': product.name,
                                    'specification_value': spec.value
                                }
                    if spec.specification.name not in spec_for_compare_list:
                        products_for_compare['specifications_for_compare'][spec.specification.name] = [spec_dict]
                    else:
                        products_for_compare['specifications_for_compare'][spec.specification.name].append(spec_dict)
                else:
                    products_for_compare['ratings'].append(
                        {
                            'product_name': product.name,
                            'rating': spec.value
                        }
                    )

        except ObjectDoesNotExist:
            return HttpResponse('Ошибка: не удалось сформировать словарь для сравнения товаров')
    return products_for_compare


def get_number_goods_for_compare() -> int:
    """
    Данная функция реализует получение кол-ва товаров, добавленных в список для сравнения
    """
    compare_object = cache.get('compare_object')
    if compare_object is None:
        return 0
    else:
        return len(compare_object['products_list'])


def get_goods_list_for_compare_view(request) -> render:
    """
    Данная функция реализует получение всех данных о товарах, добавленных в список для сравнения
    и их спецификациях.
    Вызывает функцию get_products_for_compare(), которая возвращает словарь с данными, которые передаются в шаблон

    :param request:
    """
    compare_object = cache.get('compare_object')
    products_for_compare_num = get_number_goods_for_compare()
    if compare_object is None:
        products_for_compare = None
    else:
        products_for_compare = get_products_for_compare(compare_object)
    return render(request, 'compare.html', context={'products_for_compare': products_for_compare,
                                                    'middle_title_left': 'сравнение товаров',
                                                    'middle_title_right': 'сравнение товаров',
                                                    'products_for_compare_num': products_for_compare_num})
