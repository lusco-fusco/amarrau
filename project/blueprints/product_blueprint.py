from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from project import db
from project.model.product import Product, ProductSchema
from project.model.user import User
from project.model.user_to_product import UserToProduct

product_blueprint = Blueprint('product', __name__)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@product_blueprint.route('/amarrau/v1/products', methods=['POST'])
@jwt_required
def follow_product():
    current_user = User.find_one({'id': get_jwt_identity()})
    url = request.get_json().get('url')
    trigger = request.get_json().get('trigger', -1)

    # Check product
    product = Product.find_one({'url': url})

    if product is None:
        name, current_price = Product.extract_data(url)
        product = Product(name=name, price=current_price, url=url)
        product.create()

    # Create relationship
    current_user.follow_product(product_id=product.id, difference_trigger=trigger)

    db.session.commit()
    return product_schema.dump(product), 200


@product_blueprint.route('/amarrau/v1/products/<product_id>', methods=['DELETE'])
@jwt_required
def unfollow_product(product_id):
    current_user = User.find_one({'id': get_jwt_identity()})
    relation = UserToProduct.find_one({'product_id': product_id, 'user_id': current_user.id})

    if relation is not None:
        relation.delete()
        db.session.commit()

        message = 'ok'
        code = 200
    else:
        message = 'not found'
        code = 404

    return message, code

