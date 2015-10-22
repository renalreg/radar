from radar.auth.exceptions import UserNotFound
from radar.models import User


def forgot_username(email):
    users = User.query.filter(User.email == email).all()

    if len(users) == 0:
        raise UserNotFound()

    # TODO send email with usernames
