from flask import request, current_app, abort
from radar.auth.sessions import current_user


def require_login():
    if (
        request.method != 'OPTIONS' and
        request.endpoint is not None and
        not current_app.is_public_endpoint(request.endpoint) and
        not current_user.is_authenticated()
    ):
        abort(401)
