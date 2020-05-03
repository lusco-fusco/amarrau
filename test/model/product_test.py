import time
from nose.tools import assert_is_not_none, assert_is_none, assert_equal

from project.model.product import Product
from test.abstract_test_case import AmarrauTestCase


class ProductTest(AmarrauTestCase):
    product_id = None
    product_url = 'https://amarrau.com/camisola-amarilla'
    product_name = 'camisola amarilla'

    # ----------------------------
    # Test configuration
    # ----------------------------
    def setUp(self):
        super().setUp()

        product = Product(name=self.product_name, price=18.89, url=self.product_url)
        product.create()
        self.product_id = product.id

    # ----------------------------
    # Test cases
    # ----------------------------
    def test_add_product(self):
        assert_is_not_none(self.product_id)

    def test_remove_product(self):
        product = Product.find_one({'id': self.product_id, 'enabled': True})
        product.soft_delete()
        p = Product.find_one({'id': self.product_id, 'enabled': True})
        assert_is_none(p)

    def test_update_product(self):
        new_name = 'camisola roja'
        product = Product.find_one({'id': self.product_id, 'enabled': True})
        product.name = new_name
        time.sleep(1)   # To avoid same key in record (Integrity exception)
        product.update()
        p = Product.find_one({'id': self.product_id, 'enabled': True})
        assert_equal(p.name, new_name)

    def test_find_one_by_url(self):
        p = Product.find_one({'url': self.product_url})
        assert_equal(p.id, self.product_id)

    def test_find_all_by_name(self):
        product = Product(name=self.product_name, price=18.89, url='https://amarrau-clone.com/camisola')
        product.create()

        products = Product.find_all({'name': self.product_name})
        assert_equal(len(products), 2)
