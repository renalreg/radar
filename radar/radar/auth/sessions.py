from flask import request, has_request_context, _request_ctx_stack
from itsdangerous import BadSignature, TimestampSigner
from sqlalchemy import func, not_
from werkzeug.local import LocalProxy

from radar.database import db
from radar.models.user_sessions import AnonymousSession, UserSession
from radar.models.users import User
from radar.config import get_config_value

current_user = LocalProxy(lambda: get_user())
current_user_session = LocalProxy(lambda: get_user_session())


def get_session_timeout():
    return get_config_value('SESSION_TIMEOUT')


def get_secret_key():
    return get_config_value('SECRET_KEY')


def login(username, password):
    # Username should be case insensitive
    username = username.lower()

    # Get user by username
    user = User.query\
        .filter(User.username == username)\
        .filter(not_(User.is_bot))\
        .first()

    # User not found
    if user is None:
        return None

    # Incorrect password
    if not user.check_password(password):
        return None

    # Create a new session
    user_session = UserSession()
    user_session.user = user
    user_session.date = func.now()
    user_session.ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_session.user_agent = request.headers.get('User-Agent')
    user_session.is_active = True
    db.session.add(user_session)
    db.session.commit()

    _request_ctx_stack.top.user_session = user_session

    token = generate_token_for_user_session(user_session)

    return user, token


def logout():
    if current_user_session.is_authenticated():
        current_user_session.is_active = False
        db.session.commit()
        _request_ctx_stack.top.user_session = AnonymousSession()


def logout_other_sessions():
    if current_user_session.is_authenticated():
        UserSession.query\
            .filter(UserSession.user == current_user)\
            .filter(UserSession.id != current_user_session.id)\
            .update({'is_active': False})
        db.session.commit()


def logout_user(user):
    UserSession.query\
        .filter(UserSession.user == user)\
        .update({'is_active': False})


def refresh_token(response):
    if current_user_session.is_authenticated():
        token = generate_token_for_user_session(current_user_session)
        response.headers['X-Auth-Token'] = token

    return response


def get_ip_address():
    return request.headers.get('X-Forwarded-For', request.remote_addr)


def get_user_agent():
    ua = request.headers.get('User-Agent')

    if ua is not None:
        # Limit to 255 characters
        ua = ua[:255]

    return ua


def get_timestamp_signer():
    secret_key = get_secret_key()
    s = TimestampSigner(secret_key)
    return s


def generate_token_for_user_session(user_session):
    s = get_timestamp_signer()
    token = s.sign(str(user_session.id))
    return token


def get_user_session_from_header():
    token = request.headers.get('X-Auth-Token')

    if token is None:
        return None
    else:
        return get_user_session_from_token(token)


def get_user_session_from_token(token):
    s = get_timestamp_signer()

    try:
        user_session_id = int(s.unsign(token, max_age=get_session_timeout()))
    except BadSignature:
        return None

    return UserSession.query\
        .filter(UserSession.id == user_session_id)\
        .filter(UserSession.is_active)\
        .filter(UserSession.ip_address == get_ip_address())\
        .filter(UserSession.user_agent == get_user_agent())\
        .first()


def get_user_session():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user_session'):
        user_session = get_user_session_from_header()

        if user_session is not None:
            user = user_session.user

            if not user.is_enabled:
                user_session = None

        if user_session is None:
            user_session = AnonymousSession()

        _request_ctx_stack.top.user_session = user_session

    return getattr(_request_ctx_stack.top, 'user_session', None)


def get_user():
    user_session = get_user_session()
    return user_session.user
