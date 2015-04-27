from radar.models import User


def check_login(username, password):
    user = User.query.filter(User.username == username).first()

    # User exists and the password is correct
    if user is not None and user.check_password(password):
        return user