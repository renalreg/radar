import logging

from sqlalchemy import event

from radar.api import views
from radar.api.auth import force_password_change, require_login
from radar.api.auth import set_cors_headers
from radar.api.debug import debug_before_request, debug_teardown_request
from radar.api.logs import log_request
from radar.app import Radar
from radar.auth.sessions import current_user, refresh_token
from radar.database import db


class RadarAPI(Radar):
    def __init__(self, *args, **kwargs):
        super(RadarAPI, self).__init__(*args, **kwargs)

        self.public_endpoints = []

        @event.listens_for(db.session, 'before_flush')
        def before_flush(session, flush_context, instances):
            if current_user.is_authenticated():
                user_id = current_user.id

                # Set the user_id for use by the log_changes trigger
                # SET LOCAL lasts until the end of the current transaction
                # http://www.postgresql.org/docs/9.4/static/sql-set.html
                session.execute('SET LOCAL radar.user_id = :user_id', dict(user_id=user_id))

        if self.debug:
            # Debug mode
            self.before_request(debug_before_request)
            self.after_request(set_cors_headers)
            self.teardown_request(debug_teardown_request)
        else:
            # Production mode
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            self.logger.addHandler(stream_handler)

        self.before_request(require_login)
        self.before_request(force_password_change)

        self.after_request(refresh_token)
        self.after_request(log_request)

        views.setup(self)

    def add_public_endpoint(self, endpoint):
        self.public_endpoints.append(endpoint)

    def is_public_endpoint(self, endpoint):
        return endpoint in self.public_endpoints
