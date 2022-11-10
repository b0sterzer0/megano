from django.test import TestCase
from django.core.cache import cache

from ..models import TestProduct, TestCategory, TestSpecification, TestSpecificationValue
from ..views import get_products_for_compare


class AddGoodForCompareTestClass(TestCase):
    category_name_1 = 'test_category_1'
    category_name_2 = 'test_category_2'
    product_name = 'test product'
    product_name_2 = 'test product 2'
    paths_to_good_images = ['asserts/images']

    @classmethod
    def setUpClass(cls):
        super(AddGoodForCompareTestClass, cls).setUpClass()
        category = TestCategory.objects.create(name=cls.category_name_1)
        another_category = TestCategory.objects.create(name=cls.category_name_2)
        product = TestProduct(name=cls.product_name, paths_to_good_images=cls.paths_to_good_images,
                                   category=category)
        product.save()
        product = TestProduct(name=cls.product_name_2, paths_to_good_images=cls.paths_to_good_images,
                                   category=another_category)
        product.save()

    def test_ordinary_situation(self):
        product_id = 1
        resp = self.client.get(f'/comparison/add/{product_id}/')
        self.assertEqual(resp.status_code, 302)
        compare_object = cache.get('compare_object')
        self.assertTrue(compare_object)
        self.assertEqual(compare_object['products_list'][0], product_id)
        cache.clear()

    def test_another_category(self):
        product_id = 1
        resp = self.client.get(f'/comparison/add/{product_id}/')
        product_id = 2
        resp = self.client.get(f'/comparison/add/{product_id}/')
        self.assertEqual(resp.status_code, 400)
        cache.clear()

    def test_more_than_four_items(self):
        product_id = 1
        for _ in range(5):
            self.client.get(f'/comparison/add/{product_id}/')
        compare_object = cache.get('compare_object')
        self.assertEqual(len(compare_object['products_list']), 4)
        cache.clear()


class RemoveGoodForCompareTestClass(TestCase):
    category_name = 'test category'
    product_name = 'test product'
    product_name_2 = 'test product 2'
    paths_to_good_images = ['asserts/images']

    @classmethod
    def setUpClass(cls):
        super(RemoveGoodForCompareTestClass, cls).setUpClass()
        category = TestCategory.objects.create(name=cls.category_name)
        product_1 = TestProduct(name=cls.product_name, paths_to_good_images=cls.paths_to_good_images,
                              category=category)
        product_1.save()
        product_2 = TestProduct(name=cls.product_name_2, paths_to_good_images=cls.paths_to_good_images,
                                category=category)
        product_2.save()
        cache.set('compare_object', {
            'category_for_compare': category,
            'products_list': [product_1.id, product_2.id]
        })

    def test_set_up_data(self):
        compare_object = cache.get('compare_object')
        self.assertEqual(len(compare_object), 2)

    def test_ordinary_situation(self):
        product_id = 6
        resp = self.client.get(f'/comparison/remove/{product_id}/')
        self.assertEqual(resp.status_code, 302)
        compare_object = cache.get('compare_object')
        self.assertEqual(compare_object['products_list'][0], 7)

    def test_zero_items(self):
        product_id = 7
        resp = self.client.get(f'/comparison/remove/{product_id}/')
        self.assertEqual(resp.status_code, 302)
        compare_object = cache.get('compare_object')
        self.assertFalse(compare_object)
        cache.clear()


class GetProductsForCompareTestClass(TestCase):
    category_name = 'test category'
    product_name_1 = 'test product 1'
    product_name_2 = 'test product 2'
    product_name_3 = 'test product 3'
    paths_to_good_images = ['asserts/images']
    spec_name = 'test_spec_name'
    spec_value = 'test_spec_value'
    spec_code = 'test_spec_code'
    spec_uom = 'test_spec_uom'

    @classmethod
    def setUpClass(cls):
        super(GetProductsForCompareTestClass, cls).setUpClass()
        category = TestCategory.objects.create(name=cls.category_name)
        product_1 = TestProduct.objects.create(name=cls.product_name_1, paths_to_good_images=cls.paths_to_good_images,
                                               category=category)
        product_2 = TestProduct.objects.create(name=cls.product_name_2, paths_to_good_images=cls.paths_to_good_images,
                                               category=category)
        product_3 = TestProduct.objects.create(name=cls.product_name_3, paths_to_good_images=cls.paths_to_good_images,
                                               category=category)
        spec = TestSpecification.objects.create(code=cls.spec_code, name=cls.spec_name, uom=cls.spec_uom)
        TestSpecificationValue.objects.create(specification=spec, value=cls.spec_value, product=product_1)
        TestSpecificationValue.objects.create(specification=spec, value=cls.spec_value, product=product_2)
        TestSpecificationValue.objects.create(specification=spec, value=cls.spec_value, product=product_3)
        cache.set('compare_objects', {
            'category_for_compare': category,
            'products_list': [product_1.id, product_2.id, product_3.id]
        })

    def test_ordinary_situation(self):
        compare_object = cache.get('compare_objects')
        self.assertTrue(compare_object)
        products_for_compare = get_products_for_compare(compare_object)
        self.assertTrue(products_for_compare)
        self.assertEqual(len(products_for_compare['products']), 3)
        self.assertEqual(len(products_for_compare['specifications_for_compare']), 1)
        self.assertTrue(products_for_compare['specifications_for_compare'][self.spec_name])
        self.assertEqual(len(products_for_compare['specifications_for_compare'][self.spec_name]), 3)
        self.assertEqual(len(products_for_compare['ratings']), 0)
