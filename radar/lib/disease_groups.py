from radar.models.disease_groups import DiseaseGroup, DiseaseGroupUser


def get_disease_groups_for_user(user):
    return get_disease_groups_for_user_with_permissions(user)


def get_disease_groups_for_user_with_permissions(user, permissions=None):
    if permissions is None:
        permissions = []

    query = DiseaseGroup.query

    if not user.is_admin:
        query = query.join(DiseaseGroup.users).filter(DiseaseGroupUser.user == user)

        for permission in permissions:
            query = query.filter(permission)

    return query.order_by(DiseaseGroup.name).all()
