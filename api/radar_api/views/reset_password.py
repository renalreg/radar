from flask import Response

from radar.auth.forgot_password import UserNotFound, reset_password, InvalidToken
from radar.serializers.core import Serializer
from radar.serializers.fields import StringField
from radar.validation.core import ValidationError
from radar.validation.reset_password import ResetPasswordValidation
from radar.views.core import ApiView, request_json


class ResetPasswordSerializer(Serializer):
    token = StringField()
    username = StringField()
    password = StringField()


class ResetPasswordView(ApiView):
    @request_json(ResetPasswordSerializer, ResetPasswordValidation)
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
