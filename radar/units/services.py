from radar.units.models import Unit
from radar.users.models import UnitUser


def get_units_for_user(user):
    return get_units_for_user_with_permissions(user)


def get_units_for_user_with_permissions(user, permissions=None):
    if permissions is None:
        permissions = []

    query = Unit.query

    if not user.is_admin:
        query = query.join(Unit.users).filter(UnitUser.user == user)

        for permission in permissions:
            query = query.filter(permission)

    return query.order_by(Unit.name).all()