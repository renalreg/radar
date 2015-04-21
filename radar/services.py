from radar.database import db_session
from radar.models import Patient, Unit, UnitUser, DiseaseGroup, DiseaseGroupUser, User


def is_user_in_disease_group(user, disease_group):
    if user.is_admin:
        return True

    dg_user = DiseaseGroupUser.query.filter(
        DiseaseGroupUser.user_id == user.id,
        DiseaseGroupUser.disease_group_id == disease_group.id
    ).first()

    return dg_user is not None

def is_user_in_unit(user, unit):
    if user.is_admin:
        return True

    unit_user = UnitUser.query.filter(
        UnitUser.user_id == user.id,
        UnitUser.unit_id == unit.id
    ).first()

    return unit_user is not None

def get_unit_filters_for_user(user):
    query = db_session.query(Unit)

    if not user.is_admin:
        # Unit users can filter by the units they belong to
        query = query.join(Unit.users).filter(UnitUser.user == user)

    return query.order_by(Unit.name).all()

def get_disease_group_filters_for_user(user):
    query = db_session.query(DiseaseGroup)

    # Admin users can filter by any disease group
    # Unit users can filter patients in their unit by any disease group
    if len(user.units) == 0 and not user.is_admin:
        # Disease group users can only filter by disease groups they belong to
        query = query.join(DiseaseGroup.users).filter(DiseaseGroupUser.user == user)

    return query.order_by(DiseaseGroup.name).all()

def get_units_for_user(user):
    query = db_session.query(Unit)

    if not user.is_admin:
        query = query.join(Unit.users).filter(UnitUser.user == user)

    return query.order_by(Unit.name).all()

def get_disease_groups_for_user(user):
    query = db_session.query(DiseaseGroup)

    if not user.is_admin:
        query = query.join(DiseaseGroup.users).filter(DiseaseGroupUser.user == user)

    return query.order_by(DiseaseGroup.name).all()

def get_unit_for_user(user, unit_id):
    query = db_session.query(Unit).filter(Unit.id == unit_id)

    if not user.is_admin:
        query = query.join(Unit.users).filter(UnitUser.user == user)

    return query.first()

def get_disease_group_for_user(user, disease_group_id):
    query = db_session.query(DiseaseGroup).filter(DiseaseGroup.id == disease_group_id)

    if not user.is_admin:
        query = query.join(DiseaseGroup.users).filter(DiseaseGroupUser.user == user)

    return query.first()

def get_users_for_user(user, search):
    # TODO
    return User.query.all()

def get_user_for_user(user, user_id):
    # TODO
    return User.query.get(user_id)

def get_patient_for_user(user, patient_id):
    # TODO
    return Patient.query.get(patient_id)

def check_login(username, password):
    user = User.query.filter(User.username == username).first()

    # User exists and the password is correct
    if user is not None and user.check_password(password):
        return user

def filter_patient_units_for_user(patient, user):
    user_units = set([unit_user.unit_id for unit_user in user.units])

    # The user can view all of the patient's units if:
    # * The user is an admin
    # * The patient belongs to one of the user's units
    if user.is_admin or any(unit_patient.unit_id in user_units for unit_patient in patient.units):
        units = list(patient.units)
    else:
        units = list()

    # Sort by unit name
    return sorted(units, key=lambda x: x.unit.name)

def filter_patient_disease_groups_for_user(patient, user):
    user_units = set([unit_user.unit_id for unit_user in user.units])

    # The user can view all of the patient's disease groups if:
    # * The user is an admin
    # * The patient belongs to one of the user's units
    if user.is_admin or any(unit_patient.unit_id in user_units for unit_patient in patient.units):
        disease_groups = list(patient.disease_groups)
    else:
        # Otherwise intersect the disease groups of the patient and the user
        user_disease_groups = set([dg_user.disease_group_id for dg_user in user.disease_groups])
        disease_groups = [x for x in patient.disease_groups if x.disease_group_id in user_disease_groups]

    # Sort by disease group name
    return sorted(disease_groups, key=lambda x: x.disease_group.name)

def filter_user_disease_groups_for_user(user, current_user):
    # TODO
    return user.disease_groups

def filter_user_units_for_user(user, current_user):
    # TODO
    return user.units

def can_user_view_demographics(user):
    # Admin users and unit users can view demographics
    return user.is_admin or len(user.units) > 0

def can_user_view_patient_demographics(user, patient):
    # User and patient are in same unit
    return len(filter_patient_units_for_user(patient, user)) > 0