import os
import base64
from random import SystemRandom
import re
import string

from flask import abort, request, current_app, has_request_context, _request_ctx_stack
from flask import render_template
from flask_mail import Message
from itsdangerous import BadSignature, TimestampSigner
from werkzeug.local import LocalProxy

from radar.lib.mail import mail
from radar.lib.models.users import User, AnonymousUser

current_user = LocalProxy(lambda: get_user())

PUBLIC_ENDPOINTS = ['login']

RESET_PASSWORD_MAX_AGE = 86400  # 1 day

# Parameters to user for password generation
GENERATE_PASSWORD_ALPHABET = string.ascii_letters + string.digits
GENERATE_PASSWORD_LENGTH = 10

PASSWORD_REGEXES = [
    '.{8,}',  # 8 characters
    '[a-z]',  # lowercase
    '[A-Z]',  # uppercase
    '[0-9]',  # number
]


def login(username, password):
    # Usernames are stored in lower case
    username = username.lower()

    # Get user by username
    user = User.query.filter(User.username == username).first()

    # User not found
    if user is None:
        return None

    # Incorrect password
    if not user.check_password(password):
        return None

    # Bots can't login
    if user.is_bot:
        return None

    _request_ctx_stack.top.user = user

    return user


def generate_reset_password_token():
    return base64.urlsafe_b64encode(os.urandom(32))


def send_reset_password_email(user, token):
    # TODO url
    url = 'TODO'

    msg = Message('RaDaR Reset Password', recipients=[user.email])
    msg.html = render_template('emails/reset_password.html', user=user, url=url)
    mail.send(msg)


def send_username_reminder_email(email, users):
    # TODO include RaDaR URL
    msg = Message('RaDaR Username Reminder', recipients=[email])
    msg.html = render_template('emails/username_reminder.html', email=email, users=users)
    mail.send(msg)


def generate_password():
    return ''.join(SystemRandom().sample(GENERATE_PASSWORD_ALPHABET, GENERATE_PASSWORD_LENGTH))


def check_password_policy(password):
    for regex in PASSWORD_REGEXES:
        if not re.search(regex, password):
            return False

    return True


def require_login():
    if request.method != 'OPTIONS' and request.endpoint not in PUBLIC_ENDPOINTS and not current_user.is_authenticated():
        abort(401)


def generate_token(user):
    s = TimestampSigner(current_app.config['SECRET_KEY'])
    token = s.sign(str(user.id))
    return token


def get_user_from_header():
    token = request.headers.get('X-Auth-Token')

    if token is None:
        return None
    else:
        return get_user_from_token(token)


def get_user_from_token(token):
    s = TimestampSigner(current_app.config['SECRET_KEY'])

    try:
        user_id = int(s.unsign(token, max_age=86400))
    except BadSignature:
        return None

    return User.query.filter(User.id == user_id).first()


def get_user():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user'):
        user = get_user_from_header()

        if user is not None:
            if not user.is_enabled:
                user = None

        if user is None:
            user = AnonymousUser()

        _request_ctx_stack.top.user = user

    return getattr(_request_ctx_stack.top, 'user', None)
