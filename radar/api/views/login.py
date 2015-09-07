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


class Login(ApiView):
    def post(self):
        login_serializer = LoginSerializer()

        json = request.get_json()

        if json is None:
            raise BadRequest('Expected JSON.')

        credentials = login_serializer.to_value(json)

        user = User.query.filter(User.username == credentials['username']).first()

        if user is None:
            raise ValidationError({'username': ['User not found.']})

        if not user.check_password(credentials['password']):
            raise ValidationError({'password': ['Incorrect password.']})

        user_id = user.id

        # TODO
        s = TimestampSigner('SECRET')
        token = s.sign(str(user_id))

        token_serializer = TokenSerializer()
        data = token_serializer.to_data({'user_id': user_id, 'token': token})

        return jsonify(data), 200
