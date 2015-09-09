from functools import wraps

from flask import request, jsonify
from itsdangerous import TimestampSigner

from radar.lib.exceptions import BadRequest
from radar.lib.serializers import Serializer, StringField, IntegerField, ValidationError
from radar.lib.views import ApiView
from radar.models import User


class LoginSerializer(Serializer):
    username = StringField()
    password = StringField()


class TokenSerializer(Serializer):
    user_id = IntegerField()
    token = StringField()


def request_json(serializer_class):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            json = request.get_json()

            if json is None:
                raise BadRequest()

            serializer = serializer_class()
            data = serializer.to_value(json)

            args = list(args)
            args.append(data)

            return f(*args, **kwargs)

        return wrapper

    return decorator


def response_json(serializer_class):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)
            serializer = serializer_class()
            data = serializer.to_data(response)
            return jsonify(data), 200

        return wrapper

    return decorator


class Login(ApiView):
    @request_json(LoginSerializer)
    @response_json(TokenSerializer)
    def post(self, credentials):
        user = User.query.filter(User.username == credentials['username']).first()

        if user is None:
            raise ValidationError({'username': ['User not found.']})

        if not user.check_password(credentials['password']):
            raise ValidationError({'password': ['Incorrect password.']})

        user_id = user.id

        # TODO
        s = TimestampSigner('SECRET')
        token = s.sign(str(user_id))

        return {'user_id': user_id, 'token': token}
