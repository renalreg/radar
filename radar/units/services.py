from radar.models import Unit


def get_units_for_user(user):
    query = Unit.query.order_by(Unit.name)

    if not user.is_admin:
        query = query.join(Unit.users).filter(UnitUser.user == user).all()

    return query.all()