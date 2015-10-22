from radar.models import User


def forgot_password(username):
    user = User.query.filter(User.username == username).first()

    if user is None:
        return False

    return True
