from nose.tools import assert_true, assert_is_not_none, assert_raises, assert_equal, assert_is_none
from sqlalchemy.exc import IntegrityError

from project.model.role import RoleName
from project.model.user import User
from test.abstract_test_case import AmarrauTestCase


class UserTest(AmarrauTestCase):
    default_email = 'default_user@amarrau.com'
    default_password = 'p4sSw0rD'
    default_id = None

    # ----------------------------
    # Test configuration
    # ----------------------------
    def setUp(self):
        super().setUp()
        user = User(email=self.default_email, first_name='default', last_name='user')
        user.hash_password(self.default_password)
        user.create()
        self.default_id = user.id

    # ----------------------------
    # Test cases
    # ----------------------------
    def test_create_user(self):
        user = User(email='user@amarrau.com', first_name='user_name', last_name='user_last')
        user.hash_password('p4sSw0rD')
        user.create()
        assert_is_not_none(user.id)

    def test_create_user_without_password(self):
        with assert_raises(IntegrityError):
            user = User(email='user@amarrau.com', first_name='user_name', last_name='user_last')
            user.create()

    def test_create_user_with_existing_email(self):
        with assert_raises(IntegrityError):
            user = User(email=self.default_email, first_name='user_name', last_name='user_last')
            user.create()

    def verify_password(self):
        user = User.find_one({'email': self.default_email})
        assert_true(user.verify_password(self.default_password))

    def test_update_user(self):
        new_name = 'new_name'

        user = User.find_one({'email': self.default_email})
        user.first_name = new_name
        user.update()

        assert_equal(new_name, user.first_name)
        assert_is_not_none(user.modification_date)

    def test_update_user_with_existing_email(self):
        email = 'user@amarrau.com'

        user = User(email=email, first_name='user_name', last_name='user_last')
        user.hash_password('p4sSw0rD')
        user.create()

        with assert_raises(IntegrityError):
            user.email = self.default_email
            user.update()

    def test_remove_user(self):
        user = User.find_one({'email': self.default_email})
        user.soft_delete()
        retrieved_user = User.find_one({'email': self.default_email, 'enabled': True})
        assert_is_none(retrieved_user)

    def test_remove_user_and_create_one_same_email(self):
        user = User.find_one({'email': self.default_email})
        user.soft_delete()

        u = User(email=self.default_email, first_name='user_name', last_name='user_last')
        u.hash_password('p4sSw0rD')
        u.create()

    def test_find_one_by_email(self):
        user = User.find_one({'email': self.default_email})
        assert_equal(user.email, self.default_email)
        assert_is_not_none(user)

    def test_find_one_by_id(self):
        user = User.find_one({'id': self.default_id})
        assert_is_not_none(user)

    def test_find_all_and_filter_by_role(self):
        user1 = User(email='user1@amarrau.com', first_name='user_name', last_name='user_last')
        user1.hash_password(self.default_password)
        user1.create()

        user2 = User(email='user2@amarrau.com', first_name='user_name', last_name='user_last')
        user2.hash_password(self.default_password)
        user2.create()

        admin = User(email='admin@amarrau.com', first_name='admin', last_name='user_last', role=RoleName.ADMIN)
        admin.hash_password(self.default_password)
        admin.create()

        users = User.find_all({'role': RoleName.USER})
        assert_equal(len(users), 3)

        admins = User.find_all({'role': RoleName.ADMIN})
        assert_equal(len(admins), 1)

        all_users = User.find_all()
        assert_equal(len(all_users), 4)
