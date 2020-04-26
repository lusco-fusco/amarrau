from project import db
from sqlalchemy.sql.schema import UniqueConstraint

from project.model.abstract.abstract_model import AbstractModel


# -------------------------------------
# SQLAlchemy Entities
# -------------------------------------
class UserToProduct(db.Model, AbstractModel):
    product_id = db.Column(db.String(40), db.ForeignKey("product.id"), primary_key=True)
    user_id = db.Column(db.String(250), db.ForeignKey("user.id"), primary_key=True)
    difference_trigger = db.Column(db.Integer(), nullable=True)
    user = db.relationship("User")
    product = db.relationship("Product")
    __table_args__ = (UniqueConstraint('user_id', 'product_id', name='_email_product_uc'),)

    @classmethod
    def filter(cls, filters):
        query = AbstractModel.filter(cls, filters)

        if 'product_id' in filters:
            query = query.filter_by(product_id=filters['product_id'])
        if 'user_id' in filters:
            query = query.filter_by(user_id=filters['user_id'])

        return query
