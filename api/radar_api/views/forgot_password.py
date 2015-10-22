from flask import Response
from radar.auth.forgot_password import forgot_password

from radar.serializers.core import Serializer
from radar.serializers.fields import StringField
from radar.validation.core import ValidationError
from radar.validation.forgot_password import ForgotPasswordValidation
from radar.views.core import ApiView, request_json


class ForgotPasswordSerializer(Serializer):
    username = StringField()


class ForgotPasswordView(ApiView):
    @request_json(ForgotPasswordSerializer, ForgotPasswordValidation)
    def post(self, data):
        username = data['username']

        if not forgot_password(username):
            raise ValidationError({'username': 'No user found with that username.'})

        return Response(status=200)


def register_views(app):
    app.add_public_endpoint('forgot_password')
    app.add_url_rule('/forgot-password', view_func=ForgotPasswordView.as_view('forgot_password'))
