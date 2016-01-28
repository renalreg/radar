from flask import request, current_app, abort
from radar.auth.sessions import current_user


def require_login():
    # User trying to access an endpoint that requires login
    if (
        request.method != 'OPTIONS' and
        request.endpoint is not None and
        not current_user.is_authenticated() and
        not current_app.is_public_endpoint(request.endpoint)
    ):
        abort(401)


def force_password_change():
    # Deny access to private endpoints until the user changes their password
    if (
        request.method != 'OPTIONS' and
        request.endpoint is not None and
        current_user.is_authenticated() and
        current_user.force_password_change and
        not current_app.is_public_endpoint(request.endpoint) and
        request.endpoint not in ['user_retrieve', 'user_update', 'logout']
    ):
        abort(403)


def set_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Auth-Token'
    response.headers['Access-Control-Expose-Headers'] = 'X-Auth-Token'
    return response
