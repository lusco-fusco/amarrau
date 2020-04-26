from datetime import datetime, timedelta
from enum import Enum
from secrets import token_urlsafe
from sqlalchemy import DATETIME, Enum as SQLEnum

from project import db
from project.model.abstract.abstract_model import AbstractModel


# -------------------------------------
# Utils
# -------------------------------------
def generate_token():
    """
        Generates a 32 char token

        :return: the token
    """
    return token_urlsafe(32)


def establish_expiration_date():
    """
        Generate the token expiration date

        :return: current timestamp with 5 hours added
    """
    return datetime.now() + timedelta(hours=5)


class TokenType(Enum):
    ACTIVATE_USER = 0
    RESET_PASSWORD = 1


# -------------------------------------
# SQLAlchemy Entities
# -------------------------------------
class Token(db.Model, AbstractModel):
    value = db.Column(db.String(50), default=generate_token, primary_key=True)
    type = db.Column(SQLEnum(TokenType), nullable=False)
    expiration_date = db.Column(DATETIME, default=establish_expiration_date, nullable=False)
    user_id = db.Column(db.String(40), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User")

    @classmethod
    def filter(cls, filters):
        query = AbstractModel.filter()

        if 'value' in filters:
            query = query.filter_by(value=filters['value'])
        if 'type' in filters:
            query = query.filter_by(type=filters['type'])
        if 'user_id' in filters:
            query = query.filter_by(user_id=filters['user_id'])

        return query
