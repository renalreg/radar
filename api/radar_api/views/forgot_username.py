from flask import Response

from radar.auth.forgot_username import forgot_username
from radar.serializers.core import Serializer
from radar.serializers.fields import StringField
from radar.validation.core import ValidationError
from radar.validation.forgot_username import ForgotUsernameValidation
from radar.views.core import ApiView, request_json


class ForgotUsernameSerializer(Serializer):
    email = StringField()


class ForgotUsernameView(ApiView):
    @request_json(ForgotUsernameSerializer, ForgotUsernameValidation)
    def post(self, data):
        email = data['email']

        if not forgot_username(email):
            raise ValidationError({'email': 'No users found with that email address.'})

        return Response(status=200)


def register_views(app):
    app.add_public_endpoint('forgot_username')
    app.add_url_rule('/forgot-username', view_func=ForgotUsernameView.as_view('forgot_username'))
