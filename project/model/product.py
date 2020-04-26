import requests

from project import db, ma, app
from project.model.abstract.abstract_model_with_id import AbstractModelWithId
from project.model.record import Record


# -------------------------------------
# SQLAlchemy Entities
# -------------------------------------
class Product(db.Model, AbstractModelWithId):
    name = db.Column(db.Text(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    url = db.Column(db.Text(), nullable=False)
    records = db.relationship('Record', uselist=True, lazy=True)
    # followers = db.relationship('UserToProduct')

    @classmethod
    def filter(cls, filters):
        query = AbstractModelWithId.filter(cls, filters)

        if 'name' in filters:
            query = query.filter_by(name=filters['name'])
        elif 'url' in filters:
            query = query.filter_by(url=filters['url'])

        return query

    def create(self):
        super().create()
        r = Record(product_id=self.id, price=self.price)
        self.records.append(r)
        db.session.flush()

    def update(self):
        super().update()
        r = Record(product_id=self.id, price=self.price)
        self.records.append(r)
        db.session.flush()

    @staticmethod
    def extract_data(url):
        response = requests.post(app.config.get('SCOUTER_ENDPOINT'), data={"url": url}).json()
        return response.get('name'), response.get('price')


# -------------------------------------
# Marshmallow schemas
# -------------------------------------
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'url')
