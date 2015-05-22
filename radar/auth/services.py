import os
import base64

from flask import render_template, url_for
from flask_mail import Message

from radar.mail import mail
from radar.users.models import User


RESET_PASSWORD_MAX_AGE = 86400


def check_login(username, password):
    """ Authenticate a user """

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
    """ Load a user by id """

    # Get user by id, returns None if not found
    return User.query.get(user_id)


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