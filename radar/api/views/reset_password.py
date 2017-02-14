from cornflake.exceptions import ValidationError
from flask import Response

from radar.api.serializers.auth import ResetPasswordSerializer
from radar.api.views.generics import ApiView, request_json
from radar.auth.forgot_password import InvalidToken, reset_password, UserNotFound


class ResetPasswordView(ApiView):
    @request_json(ResetPasswordSerializer)
    def post(self, data):
        token = data['token']
        username = data['username']
        password = data['password']

        try:
            reset_password(token, username, password)
        except InvalidToken:
            raise ValidationError({'token': 'Your token has expired, please try again.'})
        except UserNotFound:
            raise ValidationError({'username': 'No user found with that username.'})

        return Response(status=200)


def register_views(app):
    app.add_public_endpoint('reset_password')
    app.add_url_rule('/reset-password', view_func=ResetPasswordView.as_view('reset_password'))
