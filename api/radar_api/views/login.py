from radar.auth.sessions import login, logout_other_sessions

from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, BooleanField, IntegerField
from radar.validation.core import ValidationError
from radar.validation.login import LoginValidation
from radar.views.core import ApiView, request_json, response_json


class LoginSerializer(Serializer):
    username = StringField()
    password = StringField()
    logout_other_sessions = BooleanField()


class TokenSerializer(Serializer):
    user_id = IntegerField()
    token = StringField()


class LoginView(ApiView):
    @request_json(LoginSerializer, LoginValidation)
    @response_json(TokenSerializer)
    def post(self, credentials):
        result = login(credentials['username'], credentials['password'])

        if result is None:
            raise ValidationError({'username': 'Incorrect username or password.'})

        if credentials.get('logout_other_sessions', False):
            logout_other_sessions()

        user, token = result

        return {'user_id': user.id, 'token': token}


def register_views(app):
    app.add_public_endpoint('login')
    app.add_url_rule('/login', view_func=LoginView.as_view('login'))
