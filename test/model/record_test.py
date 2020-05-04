import time

from nose.tools import assert_equal

from project.model.product import Product
from test.abstract_test_case import AmarrauTestCase


class RecordTest(AmarrauTestCase):
    product = None

    # ----------------------------
    # Test configuration
    # ----------------------------
    def setUp(self):
        super().setUp()

        self.product = Product(name='sample product', price=18.89, url='https://amarrau.com/sample-product')
        self.product.create()

    # ----------------------------
    # Test cases
    # ----------------------------
    def test_add_product_register_and_get_all_record(self):
        self.product.price = 10.00
        time.sleep(1)  # To avoid same key in record (Integrity exception)
        self.product.update()
        self.product.price = 20.00
        time.sleep(1)  # To avoid same key in record (Integrity exception)
        self.product.update()

        assert_equal(len(self.product.records), 3)
