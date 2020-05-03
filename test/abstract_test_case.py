import os

from flask_testing import TestCase
from project import app, db
from project.model.role import RoleName, Role


class AmarrauTestCase(TestCase):

    # ----------------------------
    # Test configuration
    # ----------------------------
    def create_app(self):
        database_test_uri = os.getenv("DATABASE_TEST_URI", None)
        if database_test_uri is None:
            database_test_uri = app.config.get('SQLALCHEMY_DATABASE_URI').replace('amarrau', 'test')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_test_uri
        return app

    def setUp(self):
        db.create_all()

        user = Role(name=RoleName.USER)
        admin = Role(name=RoleName.ADMIN)

        db.session.add(user)
        db.session.add(admin)
        db.session.flush()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
