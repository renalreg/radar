import base64
import os
from radar.auth.passwords import generate_password_hash
from radar.models import User

RESET_PASSWORD_MAX_AGE = 86400  # 1 day


def generate_reset_password_token():
    # Token is given to user, hash is stored
    token = base64.urlsafe_b64encode(os.urandom(32))
    token_hash = generate_password_hash(token)
    return token, token_hash


def forgot_password(username):
    user = User.query.filter(User.username == username).first()

    if user is None:
        return False

    return True
