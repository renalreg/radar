from radar.models import Unit
from radar.users.models import User, UnitUser


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