from flask import current_app
from cornflake import fields, serializers

from radar.views.generics import ApiView, response_json


class EnvironmentSerializer(serializers.Serializer):
    live = fields.BooleanField()
    session_timeout = fields.IntegerField()


class EnvironmentView(ApiView):
    @response_json(EnvironmentSerializer)
    def get(self):
        return {
            'live': current_app.config.get('LIVE', False),
            'session_timeout': current_app.config['SESSION_TIMEOUT']
        }


def register_views(app):
    app.add_public_endpoint('environment')
    app.add_url_rule('/environment', view_func=EnvironmentView.as_view('environment'))
