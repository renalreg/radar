from cornflake.exceptions import ValidationError
from flask import Response

from radar.api.serializers.auth import ForgotPasswordSerializer
from radar.api.views.generics import ApiView, request_json
from radar.auth.forgot_password import forgot_password, UserNotFound


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
