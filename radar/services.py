from sqlalchemy import or_
from sqlalchemy.orm import aliased

from radar.database import db_session
from radar.models import Patient, UnitPatient, Unit, UnitUser, DiseaseGroupPatient, DiseaseGroup, DiseaseGroupUser, User, \
    SDAPatient, SDAContainer, SDAPatientName, SDAPatientNumber


def sda_patient_sub_query(*args):
    patient_alias = aliased(Patient)
    sub_query = db_session.query(SDAPatient)\
        .join(SDAContainer)\
        .join(patient_alias)\
        .filter(Patient.id == patient_alias.id)\
        .filter(*args)\
        .exists()
    return sub_query

def sda_patient_name_sub_query(*args):
    patient_alias = aliased(Patient)
    sub_query = db_session.query(SDAPatientName)\
        .join(SDAPatient)\
        .join(SDAContainer)\
        .join(patient_alias)\
        .filter(Patient.id == patient_alias.id)\
        .filter(*args)\
        .exists()
    return sub_query

def sda_patient_number_sub_query(*args):
    patient_alias = aliased(Patient)
    sub_query = db_session.query(SDAPatientNumber)\
        .join(SDAPatient)\
        .join(SDAContainer)\
        .join(patient_alias)\
        .filter(Patient.id == patient_alias.id)\
        .filter(*args)\
        .exists()
    return sub_query

def first_name_filter(first_name):
    first_name_like = first_name + '%'

    patient_filter = sda_patient_sub_query(SDAPatient.name_given_name.like(first_name_like))
    alias_filter = sda_patient_name_sub_query(SDAPatientName.given_name.like(first_name_like))

    return or_(patient_filter, alias_filter)

def last_name_filter(last_name):
    last_name_like = last_name + '%'

    patient_filter = sda_patient_sub_query(SDAPatient.name_family_name.like(last_name_like))
    alias_filter = sda_patient_name_sub_query(SDAPatientName.family_name.like(last_name_like))

    return or_(patient_filter, alias_filter)

def date_of_birth_filter(date_of_birth):
    return sda_patient_sub_query(SDAPatient.birth_time == date_of_birth)

def patient_number_filter(number):
    # One of the patient's identifiers matches
    number_like = number + '%'
    number_filter = sda_patient_number_sub_query(SDAPatientNumber.number.like(number_like))

    # RaDaR ID matches
    radar_filter = Patient.id == number

    return or_(number_filter, radar_filter)

def gender_filter(gender_code):
    return sda_patient_sub_query(SDAPatient.gender_code == gender_code)

def get_patients_for_user(user, search=None):
    # True if this query is filtering on demographics
    querying_demographics = False

    query = db_session.query(Patient)

    if search is not None:
        first_name = search.get('first_name')
        last_name = search.get('last_name')
        date_of_birth = search.get('date_of_birth')
        gender = search.get('gender')
        identifier = search.get('identifier')

        if first_name:
            querying_demographics = True
            query = query.filter(first_name_filter(first_name))

        if last_name:
            querying_demographics = True
            query = query.filter(last_name_filter(last_name))

        if date_of_birth:
            querying_demographics = True
            query = query.filter(date_of_birth_filter(date_of_birth))

        if gender:
            query = query.filter(gender_filter(gender))

        if identifier:
            querying_demographics = True
            query = query.filter(patient_number_filter(identifier))

        # Filter by unit
        if search.get('unit_id'):
            unit = Unit.query.get(search.get('unit_id'))

            # Unit exists
            if unit is not None:
                # User belongs to unit
                if is_user_in_unit(user, unit):
                    querying_demographics = True
                    query = query.join(UnitPatient).filter(UnitPatient.unit == unit)

        # Filter by disease group
        if search.get('disease_group_id'):
            # Get the disease group with this id
            disease_group = DiseaseGroup.query.get(search.get('disease_group_id'))

            # Disease group exists
            if disease_group is not None:
                # If the user doesn't belong to the disease group they need unit permissions
                if not is_user_in_disease_group(user, disease_group):
                    querying_demographics = True

                # Filter by disease group
                query = query.join(DiseaseGroupPatient).filter(DiseaseGroupPatient.disease_group == disease_group)

    patient_unit_alias = aliased(Patient)
    permission_through_unit_subq = db_session.query(patient_unit_alias)\
        .join(patient_unit_alias.units)\
        .join(UnitPatient.unit)\
        .join(Unit.users)\
        .filter(UnitUser.user_id == user.id, patient_unit_alias.id == Patient.id)\
        .exists()

    if querying_demographics:
        permission_filter = permission_through_unit_subq
    else:
        patient_disease_group_alias = aliased(Patient)
        permission_through_disease_group_subq = db_session.query(patient_disease_group_alias)\
            .join(patient_disease_group_alias.disease_groups)\
            .join(DiseaseGroupPatient.disease_group)\
            .join(DiseaseGroup.users)\
            .filter(DiseaseGroupUser.user_id == user.id, patient_disease_group_alias.id == Patient.id)\
            .exists()

        permission_filter = or_(permission_through_unit_subq, permission_through_disease_group_subq)

    query = query.filter(permission_filter)

    patients = query.filter(permission_filter).all()

    return patients

def is_user_in_disease_group(user, disease_group):
    dg_user = DiseaseGroupUser.query.filter(
        DiseaseGroupUser.user_id == user.id,
        DiseaseGroupUser.disease_group_id == disease_group.id
    ).first()

    return dg_user is not None

def is_user_in_unit(user, unit):
    unit_user = UnitUser.query.filter(
        UnitUser.user_id == user.id,
        UnitUser.unit_id == unit.id
    ).first()

    return unit_user is not None

def get_unit_filters_for_user(user):
    # Users can filter by the units they belong to
    return db_session.query(Unit)\
        .join(Unit.users)\
        .filter(UnitUser.user == user)\
        .all()

def get_disease_group_filters_for_user(user):
    # User belongs to a unit
    if len(user.units) > 0:
        # Unit user can filter patients in their unit by any disease group
        return db_session.query(DiseaseGroup)\
            .order_by(DiseaseGroup.name)\
            .all()
    else:
        # Disease group users can only filter by disease groups they belong to
        return db_session.query(DiseaseGroup)\
            .join(DiseaseGroup.users)\
            .filter(DiseaseGroupUser.user == user)\
            .order_by(DiseaseGroup.name)\
            .all()

def get_units_for_user(user):
    return db_session.query(Unit)\
        .join(Unit.users)\
        .filter(UnitUser.user == user)\
        .order_by(Unit.name)\
        .all()

def get_disease_groups_for_user(user):
    return db_session.query(DiseaseGroup)\
        .join(DiseaseGroup.users)\
        .filter(DiseaseGroupUser.user == user)\
        .order_by(DiseaseGroup.name)\
        .all()

def get_unit_for_user(user, unit_id):
    return db_session.query(Unit)\
        .join(Unit.users)\
        .filter(
            Unit.id == unit_id,
            UnitUser.user == user
        )\
        .first()

def get_disease_group_for_user(user, disease_group_id):
    return db_session.query(DiseaseGroup)\
        .join(DiseaseGroup.users)\
        .filter(
            DiseaseGroup.id == disease_group_id,
            DiseaseGroupUser.user == user
        )\
        .first()

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

def can_user_view_demographics(user, patient):
    # TODO
    return True

def filter_patient_units_for_user(patient, user):
    user_units = set([unit_user.unit_id for unit_user in user.units])

    # If the patient belongs to one of the user's units, the user can view all of the patient's units
    if any(unit_patient.unit_id in user_units for unit_patient in patient.units):
        units = list(patient.units)
    else:
        units = list()

    # Sort by unit name
    return sorted(units, key=lambda x: x.unit.name)

def filter_patient_disease_groups_for_user(patient, user):
    user_units = set([unit_user.unit_id for unit_user in user.units])

    # If the patient belongs to one of the user's units, the user can view all of the patient's disease groups
    if any(unit_patient.unit_id in user_units for unit_patient in patient.units):
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