from radar.disease_groups.models import DiseaseGroup
from radar.units.models import Unit
from radar.users.models import User
from radar.users.roles import UNIT_ROLES, DISEASE_GROUP_ROLES, UNIT_MANAGED_ROLES, DISEASE_GROUP_MANAGED_ROLES


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


def get_managed_units(user):
    # TODO
    return Unit.query.order_by(Unit.name).all()


def get_managed_disease_groups(user):
    # TODO
    return DiseaseGroup.query.order_by(DiseaseGroup.name).all()