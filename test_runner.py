import unittest

# --------------------------------
# Adding test cases
# --------------------------------
# Model test
from test.model.user_test import UserTest
from test.model.product_test import ProductTest
from test.model.user_to_product_test import UserToProductTest
from test.model.record_test import RecordTest
# Blueprint test
from test.blueprints.user_blueprint_test import UserBlueprintTest

if __name__ == '__main__':
    unittest.main()
