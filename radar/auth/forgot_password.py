import base64
from datetime import datetime
import os

from radar.auth.exceptions import InvalidToken, UserNotFound
from radar.auth.passwords import check_password_hash, generate_password_hash
from radar.auth.sessions import logout_user
from radar.config import config
from radar.database import db
from radar.mail import send_email_from_template
from radar.models.users import User


def get_password_reset_max_age():
    return config["PASSWORD_RESET_MAX_AGE"]


def get_base_url():
    return config["BASE_URL"]


def generate_reset_password_token():
    # Token is given to user, hash is stored
    token = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8")
    token_hash = generate_password_hash(token)
    return token, token_hash


def forgot_password(username, email):
    user = User.query.filter(User.username == username, User.email == email).first()

    # User not found
    if user is None:
        raise UserNotFound()

    token, token_hash = generate_reset_password_token()

    user.reset_password_token = token_hash
    user.reset_password_date = datetime.now()  # TODO timezone?

    db.session.commit()

    send_reset_password_email(user, token)


def send_reset_password_email(user, token):
    base_url = get_base_url()
    reset_password_url = base_url + "/reset-password/%s" % token

    send_email_from_template(
        user.email,
        "RaDaR Password Reset",
        "reset_password",
        {"reset_password_url": reset_password_url, "user": user},
    )


def reset_password(token, username, password):
    user = User.query.filter(User.username == username).first()

    # User not found
    if user is None:
        raise UserNotFound()

    # User hasn't reset their password
    if user.reset_password_token is None:
        raise InvalidToken()

    # Token doesn't match
    if not check_password_hash(user.reset_password_token, token):
        raise InvalidToken()

    max_age = get_password_reset_max_age()

    # Token has expired
    # TODO timezone?
    if (
        user.reset_password_date is not None
        and (datetime.now() - user.reset_password_date).total_seconds() > max_age
    ):
        raise InvalidToken()

    # Update the user's password
    user.password = password

    # Logout all of the user's sessions
    logout_user(user)

    # Clear the reset password token
    user.reset_password_token = None
    user.reset_password_date = None

    # Unset the force password change flag
    user.force_password_change = False

    db.session.commit()
