import os
import base64
from random import SystemRandom
import re
import string

from flask import render_template, url_for
from flask_mail import Message

from radar.lib.mail import mail
from radar.models.users import User


# Flask endpoints that don't require login
PUBLIC_ENDPOINTS = [
    'radar.index',
    'auth.login',
    'auth.forgot_username',
    'auth.forgot_password',
    'auth.reset_password',
    'static',
    'news.view_posts',
    'news.view_post',
]

# Flask endpoints that can be accessed while the user has the force password change flag set
FORCE_PASSWORD_CHANGE_ENDPOINTS = [
    'auth.change_password',
    'auth.logout',
    'static'
]

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
PASSWORD_POLICY = 'Must be at least 8 characters and include: a lowercase letter, an uppercase letter and a digit.'


def check_login(username, password):
    """ Authenticate a user """

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

    # Authentication was successful
    return user


def load_user(user_id):
    """ Load a user by id, returns None if not found """

    user = User.query.get(user_id)

    # Get user by id,
    return user


def generate_reset_password_token():
    return base64.urlsafe_b64encode(os.urandom(32))


def send_reset_password_email(user, token):
    url = url_for('auth.reset_password', token=token, _external=True)

    msg = Message('RaDaR Reset Password', recipients=[user.email])
    msg.html = render_template('emails/reset_password.html', user=user, url=url)
    mail.send(msg)


def send_username_reminder_email(email, users):
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
