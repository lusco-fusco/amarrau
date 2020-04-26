from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from project.model.user import UserSchema, User

profile_blueprint = Blueprint('profile', __name__)
user_schema = UserSchema()


@profile_blueprint.route('/amarrau/v1/profile', methods=['GET'])
@jwt_required
def retrieve_profile():
    return user_schema.dump(User.find_one({'id': get_jwt_identity()})), 200


@profile_blueprint.route('/amarrau/v1/profile', methods=['PATCH'])
@jwt_required
def update_profile():
    current_user = User.find_one({'id': get_jwt_identity()})

    current_user.email = request.get_json().get('email', current_user.email)
    current_user.first_name = request.get_json().get('first_name', current_user.first_name)
    current_user.last_name = request.get_json().get('last_name', current_user.last_name)

    current_user.update()

    return user_schema.dump(current_user), 200


@profile_blueprint.route('/amarrau/v1/profile/password', methods=['PATCH'])
@jwt_required
def update_password():
    current_user = User.find_one({'id': get_jwt_identity()})

    if request.get_json().get('password') == request.get_json().get('password_confirm'):
        current_user.hash_password(request.get_json().get('password'))
        current_user.update()
        message = 'ok'
        code = 200
    else:
        message = 'password does not match'
        code = 409

    return message, code


@profile_blueprint.route('/amarrau/v1/profile', methods=['DELETE'])
@jwt_required
def delete_profile():
    current_user = User.find_one({'id': get_jwt_identity()})

    if current_user.verify_password(request.get_json().get('password')):
        # TODO: Remove tokens in redis
        current_user.soft_delete()
        message = 'ok'
        code = 200
    else:
        message = 'password incorrect'
        code = 401

    return message, code
