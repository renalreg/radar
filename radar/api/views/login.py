from cornflake.exceptions import ValidationError

from radar.auth.sessions import (
    login,
    logout_other_sessions,
    DisabledLoginError,
    UsernameLoginError,
    PasswordLoginError
)
from radar.api.serializers.auth import LoginSerializer, TokenSerializer
from radar.api.views.generics import ApiView, request_json, response_json


class LoginView(ApiView):
    @request_json(LoginSerializer)
    @response_json(TokenSerializer)
    def post(self, credentials):
        try:
            user, token = login(credentials['username'], credentials['password'])
        except DisabledLoginError:
            raise ValidationError({'username': 'Account disabled, please contact support.'})
        except (UsernameLoginError, PasswordLoginError):
            raise ValidationError({'username': 'Incorrect username or password.'})

        if credentials.get('logout_other_sessions', False):
            logout_other_sessions()

        return {'user_id': user.id, 'token': token}


def register_views(app):
    app.add_public_endpoint('login')
    app.add_url_rule('/login', view_func=LoginView.as_view('login'))
