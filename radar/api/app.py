import logging

from sqlalchemy import event

from radar.api import views
from radar.app import Radar
from radar.api.auth import require_login, force_password_change
from radar.api.auth import set_cors_headers
from radar.api.debug import debug_before_request, debug_teardown_request
from radar.api.logs import log_request
from radar.auth.sessions import refresh_token, current_user
from radar.database import db
from radar.template_filters import register_template_filters


class RadarApi(Radar):
    def __init__(self, *args, **kwargs):
        super(RadarApi, self).__init__(*args, **kwargs)

        self.public_endpoints = []

        @event.listens_for(db.session, 'before_flush')
        def before_flush(session, flush_context, instances):
            if current_user.is_authenticated():
                user_id = current_user.id

                # SET LOCAL lasts until the end of the current transaction
                # http://www.postgresql.org/docs/9.4/static/sql-set.html
                session.execute('SET LOCAL radar.user_id = :user_id', dict(user_id=user_id))

        if self.debug:
            self.before_request(debug_before_request)
            self.after_request(set_cors_headers)
            self.teardown_request(debug_teardown_request)
        else:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            self.logger.addHandler(stream_handler)

        self.before_request(require_login)
        self.before_request(force_password_change)

        self.after_request(refresh_token)
        self.after_request(log_request)

        register_template_filters(self)

        views.setup(self)

    def setup_config(self):
        self.config.from_object('radar.default_settings')
        self.config.from_object('radar.api.default_settings')
        self.config.from_envvar('RADAR_SETTINGS')

    def add_public_endpoint(self, endpoint):
        self.public_endpoints.append(endpoint)

    def is_public_endpoint(self, endpoint):
        return endpoint in self.public_endpoints
