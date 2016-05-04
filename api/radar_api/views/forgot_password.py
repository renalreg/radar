from flask import Response
from radar.auth.forgot_password import forgot_password, UserNotFound

from radar.validation.core import ValidationError
from radar.views.core import ApiView, request_json


class ForgotPasswordView(ApiView):
    @request_json(ForgotPasswordSerializer)
    def post(self, data):
        username = data['username']
        email = data['email']

        try:
            forgot_password(username, email)
        except UserNotFound:
            raise ValidationError({'username': 'No user found with that username and email.'})

        return Response(status=200)


def register_views(app):
    app.add_public_endpoint('forgot_password')
    app.add_url_rule('/forgot-password', view_func=ForgotPasswordView.as_view('forgot_password'))
