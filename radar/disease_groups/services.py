from radar.models import DiseaseGroup
from radar.users.models import DiseaseGroupUser


def get_disease_groups_for_user(user):
    query = DiseaseGroup.query.order_by(DiseaseGroup.name)

    if not user.is_admin:
        query = query.join(DiseaseGroup.users).filter(DiseaseGroupUser.user == user).all()

    return query.all()