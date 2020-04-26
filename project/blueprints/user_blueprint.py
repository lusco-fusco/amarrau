from flask import Blueprint, request, abort, Response

from project import db
from project.model.user import UserSchema, User

user_blueprint = Blueprint("user", __name__)
user_schema = UserSchema()


@user_blueprint.route("/amarrau/v1/register", methods=['POST'])
def register_user():
    # Gets params
    email = request.json.get('email')
    password = request.json.get('password')
    password_confirm = request.json.get('password_confirm')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')

    # Checks password
    if password != password_confirm:
        abort(409, Response('Passwords do not match'))

    # Checks integrity
    user_to_check = User.find_one({'email': email, 'enabled': True})

    if user_to_check is None:
        # Creates user
        user = User(email=email, first_name=first_name, last_name=last_name)
        user.hash_password(password)
        user.create()

        # Persists it
        db.session.commit()

        message = user_schema.dump(user)
        code = 200
    else:
        message = '{} email is not available'.format(email)
        code = 409

    return message, code
