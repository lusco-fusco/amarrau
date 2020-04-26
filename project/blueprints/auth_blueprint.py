from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti, jwt_required, get_raw_jwt, \
    jwt_refresh_token_required, get_jwt_identity

from project import jwt, redis, ConfigJWT
from project.model.user import UserSchema, User

auth_blueprint = Blueprint("auth", __name__)
user_schema = UserSchema()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis.get(jti)
    if entry is None:
        return True
    return entry == 'true'

# TODO: If user does not exist or is not enabled return custom error
@auth_blueprint.route("/amarrau/v1/login", methods=['POST'])
def login():
    response = dict()

    email = request.json.get('email')
    password = request.json.get('password')

    user = User.find_one({'email': email, 'enabled': True})

    if user.verify_password(password):
        # Creates session and persists it in Redis
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        access_jti = get_jti(encoded_token=access_token)
        refresh_jti = get_jti(encoded_token=refresh_token)

        redis.set(access_jti, 'false', ConfigJWT.JWT_ACCESS_TOKEN_EXPIRES * 1.2)
        redis.set(refresh_jti, 'false', ConfigJWT.JWT_REFRESH_TOKEN_EXPIRES * 1.2)

        response['access_token'] = access_token
        response['refresh_token'] = refresh_token
        response['expires_in'] = datetime.now() + ConfigJWT.JWT_ACCESS_TOKEN_EXPIRES

        code = 201
    else:
        response['message'] = 'unauthorized'
        code = 401

    return response, code


@auth_blueprint.route("/amarrau/v1/logout", methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    redis.set(jti, 'true', ConfigJWT.JWT_ACCESS_TOKEN_EXPIRES * 1.2)

    return jsonify({"msg": "Successfully logged out"}), 200


@auth_blueprint.route("/amarrau/v1/refresh", methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()

    access_token = create_access_token(identity=current_user)
    access_jti = get_jti(encoded_token=access_token)

    redis.set(access_jti, 'false', ConfigJWT.JWT_ACCESS_TOKEN_EXPIRES * 1.2)

    ret = {
        'access_token': create_access_token(identity=current_user),
        'expires_in': datetime.now() + ConfigJWT.JWT_ACCESS_TOKEN_EXPIRES
    }
    return jsonify(ret), 200


@auth_blueprint.route("/amarrau/v1/refresh/logout", methods=['DELETE'])
@jwt_refresh_token_required
def logout_refresh():
    jti = get_raw_jwt()['jti']
    redis.set(jti, 'true', ConfigJWT.JWT_ACCESS_TOKEN_EXPIRES * 1.2)

    return jsonify({"msg": "Successfully logged out"}), 200
