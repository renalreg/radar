from radar.auth.passwords import generate_password
from radar.api.serializers.auth import PasswordSerializer
from radar.api.views.generics import ApiView, response_json


class RandomPasswordView(ApiView):
    @response_json(PasswordSerializer)
    def get(self):
        password = generate_password()
        return {'password': password}


def register_views(app):
    app.add_public_endpoint('random_password')
    app.add_url_rule('/random-password', view_func=RandomPasswordView.as_view('random_password'))
