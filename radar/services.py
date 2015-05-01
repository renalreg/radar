from radar.database import db
from radar.units.models import Unit
from radar.disease_groups.models import DiseaseGroup
from radar.users.models import UnitUser, DiseaseGroupUser


def get_unit_filters_for_user(user):
    query = db.session.query(Unit)

    if not user.is_admin:
        # Unit users can filter by the units they belong to
        query = query.join(Unit.users).filter(UnitUser.user == user)

    return query.order_by(Unit.name).all()


def get_disease_group_filters_for_user(user):
    query = db.session.query(DiseaseGroup)

    # Admin users can filter by any disease group
    # Unit users can filter patients in their unit by any disease group
    if len(user.units) == 0 and not user.is_admin:
        # Disease group users can only filter by disease groups they belong to
        query = query.join(DiseaseGroup.users).filter(DiseaseGroupUser.user == user)

    return query.order_by(DiseaseGroup.name).all()