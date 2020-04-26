from enum import Enum
from sqlalchemy import Enum as SQLEnum
from project import db, ma
from marshmallow_enum import EnumField


# -------------------------------------
# Utils
# -------------------------------------
class RoleName(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'


# -------------------------------------
# SQLAlchemy Entities
# -------------------------------------
class Role(db.Model):
    name = db.Column(SQLEnum(RoleName), primary_key=True)

    @staticmethod
    def __filter(name):
        query = Role.query

        if name is not None:
            query = query.filter_by(id=name)

        return query

    @staticmethod
    def find_one(name=None):
        query = Role.__filter(name)
        return query.first()

    @staticmethod
    def find_all(name=None):
        query = Role.__filter(name)
        return query.all()


# -------------------------------------
# Marshmallow schemas
# -------------------------------------
class RoleSchema(ma.Schema):
    name = EnumField(RoleName, by_value=True)
