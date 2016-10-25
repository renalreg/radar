from cornflake.exceptions import ValidationError
from flask import Response

from radar.api.serializers.auth import ForgotUsernameSerializer
from radar.api.views.generics import ApiView, request_json
from radar.auth.exceptions import UserNotFound
from radar.auth.forgot_username import forgot_username


class ForgotUsernameView(ApiView):
    @request_json(ForgotUsernameSerializer)
    def post(self, data):
        email = data['email']

        try:
            forgot_username(email)
        except UserNotFound:
            raise ValidationError({'email': 'No users found with that email address.'})

        return Response(status=200)


def register_views(app):
    app.add_public_endpoint('forgot_username')
    app.add_url_rule('/forgot-username', view_func=ForgotUsernameView.as_view('forgot_username'))
