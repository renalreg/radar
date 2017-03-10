from flask import _request_ctx_stack, has_request_context, request, session
from itsdangerous import BadSignature, TimestampSigner
from sqlalchemy import func
from werkzeug.local import LocalProxy

from radar.config import config
from radar.database import db
from radar.models.logs import Log
from radar.models.user_sessions import AnonymousSession, UserSession
from radar.models.users import User


current_user = LocalProxy(lambda: get_user())
current_user_session = LocalProxy(lambda: get_user_session())


def get_session_timeout():
    return config['SESSION_TIMEOUT']


def get_secret_key():
    return config['SECRET_KEY']


class LoginError(Exception):
    pass


class UsernameLoginError(LoginError):
    pass


class PasswordLoginError(LoginError):
    pass


class DisabledLoginError(LoginError):
    pass


def login(username, password):
    # Username should be case insensitive
    username = username.lower()

    # Get user by username
    q = User.query
    q = q.filter(User.username == username)
    user = q.first()

    # User not found
    if user is None:
        raise UsernameLoginError()

    # User is disabled
    if not user.is_enabled:
        raise DisabledLoginError()

    # Incorrect password
    if not user.check_password(password):
        raise PasswordLoginError()

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

    # Set cookie
    session['id'] = user_session.id

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

        # Unset cookie
        session.pop('id', None)


def logout_other_sessions():
    if current_user_session.is_authenticated():
        UserSession.query\
            .filter(UserSession.user == current_user)\
            .filter(UserSession.id != current_user_session.id)\
            .delete()
        db.session.commit()


def logout_user(user):
    # Delete user sessions
    UserSession.query\
        .filter(UserSession.user == user)\
        .delete()


def refresh_token(response):
    if current_user_session.is_authenticated():
        token = generate_token_for_user_session(current_user_session)
        response.headers['X-Auth-Token'] = token
        session['id'] = current_user_session.id

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


def get_user_session_by_id(user_session_id):
    q = UserSession.query
    q = q.join(UserSession.user)
    q = q.filter(UserSession.id == user_session_id)
    q = q.filter(User.is_enabled == True)  # noqa
    return q.first()


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

    return get_user_session_by_id(user_session_id)


def get_user_session_from_cookie():
    user_session_id = session.get('id')

    if user_session_id is None:
        return None

    return get_user_session_by_id(user_session_id)


def get_user_session():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user_session'):
        # Look in the header
        user_session = get_user_session_from_header()

        # Fallback to the cookie
        if user_session is None:
            user_session = get_user_session_from_cookie()

        if user_session is not None:
            user = user_session.user

            if not user.is_enabled:
                user_session = None

        # Set the user session
        _request_ctx_stack.top.user_session = user_session

    user_session = getattr(_request_ctx_stack.top, 'user_session', None)

    if user_session is None:
        user_session = AnonymousSession()

    return user_session


def get_user():
    user_session = get_user_session()
    user = user_session.user
    return user
