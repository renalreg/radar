from flask import request, has_request_context, _request_ctx_stack
from itsdangerous import BadSignature, TimestampSigner
from sqlalchemy import func
from werkzeug.local import LocalProxy

from radar.database import db
from radar.models.user_sessions import AnonymousSession, UserSession
from radar.models.users import User
from radar.config import config
from radar.models.logs import Log

current_user = LocalProxy(lambda: get_user())
current_user_session = LocalProxy(lambda: get_user_session())


def get_session_timeout():
    return config['SESSION_TIMEOUT']


def get_secret_key():
    return config['SECRET_KEY']


def login(username, password):
    # Username should be case insensitive
    username = username.lower()

    # Get user by username
    q = User.query
    q = q.filter(User.username == username)
    q = q.filter(User.is_enabled == True)  # noqa

    user = q.first()

    # User not found
    if user is None:
        return None

    # Incorrect password
    if not user.check_password(password):
        return None

    # Update old password hashes
    if user.needs_password_rehash:
        user.password = password

    # Create a new session
    user_session = UserSession()
    user_session.user = user
    user_session.date = func.now()
    user_session.ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_session.user_agent = request.headers.get('User-Agent')
    db.session.add(user_session)

    log = Log()
    log.type = 'LOGIN'
    log.user = user
    db.session.add(log)

    db.session.commit()

    _request_ctx_stack.top.user_session = user_session

    token = generate_token_for_user_session(user_session)

    return user, token


def logout():
    if current_user_session.is_authenticated():
        db.session.delete(current_user_session)

        log = Log()
        log.type = 'LOGOUT'
        log.user = current_user
        db.session.add(log)

        db.session.commit()

        _request_ctx_stack.top.user_session = AnonymousSession()


def logout_other_sessions():
    if current_user_session.is_authenticated():
        UserSession.query\
            .filter(UserSession.user == current_user)\
            .filter(UserSession.id != current_user_session.id)\
            .delete()
        db.session.commit()


def logout_user(user):
    UserSession.query\
        .filter(UserSession.user == user)\
        .delete()


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

    q = UserSession.query
    q = q.join(UserSession.user)
    q = q.filter(UserSession.id == user_session_id)
    q = q.filter(UserSession.ip_address == get_ip_address())
    q = q.filter(UserSession.user_agent == get_user_agent())
    q = q.filter(User.is_enabled == True)  # noqa

    return q.first()


def get_user_session():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user_session'):
        user_session = get_user_session_from_header()

        if user_session is not None:
            user = user_session.user

            if not user.is_enabled:
                user_session = None

        _request_ctx_stack.top.user_session = user_session

    user_session = getattr(_request_ctx_stack.top, 'user_session', None)

    if user_session is None:
        user_session = AnonymousSession()

    return user_session


def get_user():
    user_session = get_user_session()
    user = user_session.user
    return user
