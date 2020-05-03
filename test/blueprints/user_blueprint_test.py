import uuid
from unittest import mock

from nose.tools import assert_equal

from project.model.user import User
from test.abstract_test_case import AmarrauTestCase


class UserBlueprintTest(AmarrauTestCase):
    args = {
        "email": "user@amarrau.com",
        "password": "p4sSw0rd",
        "password_confirm": "p4sSw0rd",
        "first_name": "user",
        "last_name": "amarrau"
    }

    # ----------------------------
    # Test cases
    # ----------------------------
    def test_register_user(self):
        # -----------------------------------
        def mock_find_user(params):
            return None

        def create_user_mock(user):
            _id = uuid.uuid4().hex
            return User(id=_id, email="user@amarrau.com", first_name="user", last_name="amarrau", password_hash="p4sSw0rd")
        # -----------------------------------
        with mock.patch.object(User, 'find_one', new=mock_find_user):
            with mock.patch.object(User, 'create', new=create_user_mock):
                response = self.client.post("/amarrau/v1/register", json=self.args)
                assert_equal(response.status, '200 OK')

    def test_register_existing_user(self):
        # -----------------------------------
        def mock_find_user(params):
            return User(email="user@amarrau.com", first_name="user", last_name="amarrau", password_hash="p4sSw0rd")
        # -----------------------------------
        with mock.patch.object(User, 'find_one', new=mock_find_user):
            response = self.client.post("/amarrau/v1/register", json=self.args)
            assert_equal(response.status, '409 CONFLICT')

    def test_password_does_not_match(self):
        args = {
            "email": "user@amarrau.com",
            "password": "p4sSw0rd",
            "password_confirm": "p4sSword",
            "first_name": "user",
            "last_name": "amarrau"
        }
        response = self.client.post("/amarrau/v1/register", json=args)
        assert_equal(response.status, '409 CONFLICT')
