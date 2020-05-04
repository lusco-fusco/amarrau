from nose.tools import assert_equal, assert_raises
from sqlalchemy.exc import IntegrityError

from project.model.product import Product
from project.model.user import User
from test.abstract_test_case import AmarrauTestCase


class UserToProductTest(AmarrauTestCase):
    user_id = None
    products = []

    # ----------------------------
    # Test configuration
    # ----------------------------
    def setUp(self):
        super().setUp()

        # Add users
        user = User(email='user@amarrau.com', first_name='default', last_name='user')
        user.hash_password('p4sSw0rd')
        user.create()
        self.user_id = user.id

        # Add products
        Product(name='camisola roja', price=18.89, url='https://amarrau.com/camisola-roja').create()
        Product(name='camisola verde', price=0.90, url='https://amarrau.com/camisola-verde').create()
        Product(name='camisola azul', price=1.50, url='https://amarrau.com/camisola-azul').create()
        Product(name='camisola negra', price=100.00, url='https://amarrau.com/camisola-negra').create()
        Product(name='camisola blanca', price=20.19, url='https://amarrau.com/camisola-blanca').create()

        self.products = Product.find_all()

    # ----------------------------
    # Test cases
    # ----------------------------
    def test_follow_product(self):
        user = User.find_one({'id': self.user_id})

        user.follow_product(self.products[1].id, 40)
        assert_equal(len(user.wish_list), 1)

        user.follow_product(self.products[3].id, 20)
        assert_equal(len(user.wish_list), 2)

    def test_unfollow_product(self):
        user = User.find_one({'id': self.user_id})

        user.follow_product(self.products[1].id, 40)
        assert_equal(len(user.wish_list), 1)

        user.follow_product(self.products[3].id, 20)
        assert_equal(len(user.wish_list), 2)

        user.unfollow_product(self.products[3].id)
        assert_equal(len(user.wish_list), 1)

    def test_follow_product_no_existing_product(self):
        user = User.find_one({'id': self.user_id})

        with assert_raises(IntegrityError):
            user.follow_product('productid0', 40)
