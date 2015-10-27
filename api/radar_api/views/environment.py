from flask import current_app

from radar.serializers.core import Serializer
from radar.serializers.fields import BooleanField
from radar.views.core import ApiView, response_json


class EnvironmentSerializer(Serializer):
    live = BooleanField()


class EnvironmentView(ApiView):
    @response_json(EnvironmentSerializer)
    def get(self):
        return {
            'live': current_app.config.get('LIVE', False)
        }


def register_views(app):
    app.add_public_endpoint('environment')
    app.add_url_rule('/environment', view_func=EnvironmentView.as_view('environment'))
