from sqlalchemy import Enum as SQLEnum, UniqueConstraint
from project import db, ma
from passlib.apps import custom_app_context as pwd_context
from project.model.role import RoleName
from project.model.abstract.abstract_model_with_id import AbstractModelWithId
from project.model.user_to_product import UserToProduct


# -------------------------------------
# SQLAlchemy Entities
# -------------------------------------
class User(db.Model, AbstractModelWithId):
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    role = db.Column(SQLEnum(RoleName), db.ForeignKey("role.name"), default=RoleName.USER)
    # tokens = db.relationship("Token", uselist=True)
    wish_list = db.relationship('UserToProduct', uselist=True, lazy=True)
    __table_args__ = (UniqueConstraint('email', 'remove_date', name='unique_user_email'),)

    def hash_password(self, clear_password):
        self.password_hash = pwd_context.hash(clear_password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def follow_product(self, product_id, difference_trigger=None):
        relation = UserToProduct(product_id=product_id, user_id=self.id, difference_trigger=difference_trigger)
        # relation.create()
        self.wish_list.append(relation)
        db.session.flush()

    def unfollow_product(self, product_id):
        relation = UserToProduct.find_one({'product_id': product_id, 'user_id': self.id})
        self.wish_list.remove(relation)
        # db.session.flush()

    @classmethod
    def filter(cls, filters):
        query = AbstractModelWithId.filter(cls, filters)

        if 'email' in filters:
            query = query.filter_by(email=filters['email'])
        elif 'role' in filters:
            query = query.filter_by(role=filters['role'])
        elif 'first_name' in filters:
            query = query.filter_by(first_name=filters['first_name'])

        return query


# -------------------------------------
# Marshmallow schemas
# -------------------------------------
from project.model.role import RoleSchema


class UserSchema(ma.Schema):
    roles = ma.Nested(RoleSchema, many=True)

    class Meta:
        fields = ('id', 'email', 'first_name', 'last_name', 'roles')
