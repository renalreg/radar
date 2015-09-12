from radar.lib.auth import login, generate_token

from radar.lib.serializers import Serializer, StringField, IntegerField
from radar.lib.validation.core import ValidationError
from radar.lib.views.core import ApiView, request_json, response_json


class LoginSerializer(Serializer):
    username = StringField()
    password = StringField()


class TokenSerializer(Serializer):
    user_id = IntegerField()
    token = StringField()


class LoginView(ApiView):
    @request_json(LoginSerializer)
    @response_json(TokenSerializer)
    def post(self, credentials):
        user = login(credentials['username'], credentials['password'])

        if user is None:
            raise ValidationError({'username': 'Incorrect username or password.'})

        return {'user_id': user.id, 'token': generate_token(user)}
