import datetime

from project import db, ma
from project.model.abstract.abstract_model import AbstractModel


# -------------------------------------
# SQLAlchemy Entities
# -------------------------------------
class Record(db.Model, AbstractModel):
    product_id = db.Column(db.String(40), db.ForeignKey("product.id"), primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow, primary_key=True)
    price = db.Column(db.Float(), nullable=False)


# -------------------------------------
# Marshmallow schemas
# -------------------------------------
class RecordSchema(ma.ModelSchema):
    class Meta:
        fields = ('product_id', 'date', 'price')
