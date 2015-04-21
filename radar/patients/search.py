from datetime import timedelta

from sqlalchemy import or_, extract, case, desc
from sqlalchemy.orm import aliased

from radar.database import db_session
from radar.models import Patient, UnitPatient, Unit, UnitUser, DiseaseGroupPatient, DiseaseGroup, DiseaseGroupUser, \
    SDAPatient, SDAContainer, SDAPatientName, SDAPatientNumber
from radar.services import is_user_in_unit, is_user_in_disease_group


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

def filter_by_first_name(first_name):
    first_name_like = first_name + '%'

    patient_filter = sda_patient_sub_query(SDAPatient.name_given_name.like(first_name_like))
    alias_filter = sda_patient_name_sub_query(SDAPatientName.given_name.like(first_name_like))

    return or_(patient_filter, alias_filter)

def filter_by_last_name(last_name):
    last_name_like = last_name + '%'

    patient_filter = sda_patient_sub_query(SDAPatient.name_family_name.like(last_name_like))
    alias_filter = sda_patient_name_sub_query(SDAPatientName.family_name.like(last_name_like))

    return or_(patient_filter, alias_filter)

def filter_by_date_of_birth(date_of_birth):
    day = date_of_birth.date()
    next_day = day + timedelta(days=1)
    return sda_patient_sub_query(SDAPatient.birth_time >= day, SDAPatient.birth_time < next_day)

def filter_by_patient_number(number):
    # One of the patient's identifiers matches
    number_like = number + '%'
    number_filter = sda_patient_number_sub_query(SDAPatientNumber.number.like(number_like))

    # RaDaR ID matches
    radar_id_filter = filter_by_radar_id(number)

    return or_(number_filter, radar_id_filter)

def filter_by_radar_id(radar_id):
    return Patient.id == radar_id

def filter_by_gender(gender_code):
    return sda_patient_sub_query(SDAPatient.gender_code == gender_code)

def filter_by_year_of_birth(year):
    return sda_patient_sub_query(extract('year', SDAPatient.birth_time) == year)

def filter_by_unit_permissions(user):
    patient_alias = aliased(Patient)
    sub_query = db_session.query(patient_alias)\
        .join(patient_alias.units)\
        .join(UnitPatient.unit)\
        .join(Unit.users)\
        .filter(UnitUser.user_id == user.id, patient_alias.id == Patient.id)\
        .exists()
    return sub_query

def filter_by_disease_group_permissions(user):
    patient_alias = aliased(Patient)
    sub_query = db_session.query(patient_alias)\
        .join(patient_alias.disease_groups)\
        .join(DiseaseGroupPatient.disease_group)\
        .join(DiseaseGroup.users)\
        .filter(DiseaseGroupUser.user_id == user.id, patient_alias.id == Patient.id)\
        .exists()
    return sub_query

def filter_by_demographics_permissions(user):
    return filter_by_unit_permissions(user)

def order_by_demographics_field(user, field, ascending, else_=None):
    demographics_permission_sub_query = filter_by_demographics_permissions(user)
    expression = case([(demographics_permission_sub_query, field)], else_=else_)

    if not ascending:
        expression = desc(expression)

    return expression

def order_by_field(field, ascending):
    if not ascending:
        field = desc(field)

    return field

def order_by_radar_id(ascending):
    return order_by_field(Patient.id, ascending)

def order_by_first_name(user, ascending):
    return order_by_demographics_field(user, Patient.first_name, ascending)

def order_by_last_name(user, ascending):
    return order_by_demographics_field(user, Patient.last_name, ascending)

def order_by_gender(ascending):
    return order_by_field(Patient.gender, ascending)

def order_by_date_of_birth(user, ascending):
    # Users without demographics permissions can only see the year
    year_order = order_by_field(extract('year', Patient.date_of_birth), ascending)

    # Anonymised (year) values first (i.e. treat 1999 as 1999-01-01)
    anonymised_order = order_by_demographics_field(user, 1, ascending, else_=0)

    date_of_birth_order = order_by_demographics_field(user, Patient.date_of_birth, ascending)

    return [year_order, anonymised_order, date_of_birth_order]

def filter_patients(user, query, params):
    filter_by_demographics = False

    first_name = params.get('first_name')
    last_name = params.get('last_name')
    date_of_birth = params.get('date_of_birth')
    gender = params.get('gender')
    patient_number = params.get('patient_number')
    radar_id = params.get('radar_id')
    year_of_birth = params.get('year_of_birth')
    unit_id = params.get('unit_id')
    disease_group_id = params.get('disease_group_id')

    if first_name:
        filter_by_demographics = True
        query = query.filter(filter_by_first_name(first_name))

    if last_name:
        filter_by_demographics = True
        query = query.filter(filter_by_last_name(last_name))

    if date_of_birth:
        filter_by_demographics = True
        query = query.filter(filter_by_date_of_birth(date_of_birth))

    if gender:
        query = query.filter(filter_by_gender(gender))

    if patient_number:
        filter_by_demographics = True
        query = query.filter(filter_by_patient_number(patient_number))

    if radar_id is not None:
        query = query.filter(filter_by_radar_id(radar_id))

    if year_of_birth is not None:
        query = query.filter(filter_by_year_of_birth(year_of_birth))

    # Filter by unit
    if unit_id is not None:
        unit = Unit.query.get(unit_id)

        # Unit exists
        if unit is not None:
            # User belongs to unit
            if is_user_in_unit(user, unit):
                filter_by_demographics = True
                query = query.join(UnitPatient).filter(UnitPatient.unit == unit)

    # Filter by disease group
    if disease_group_id:
        # Get the disease group with this id
        disease_group = DiseaseGroup.query.get(disease_group_id)

        # Disease group exists
        if disease_group is not None:
            # If the user doesn't belong to the disease group they need unit permissions
            if not is_user_in_disease_group(user, disease_group):
                filter_by_demographics = True

            # Filter by disease group
            query = query.join(DiseaseGroupPatient).filter(DiseaseGroupPatient.disease_group == disease_group)

    return query, filter_by_demographics

def order_patients(user, order_by, ascending):
    if order_by == 'first_name':
        return [order_by_first_name(user, ascending)]
    elif order_by == 'last_name':
        return [order_by_last_name(user, ascending)]
    elif order_by == 'gender':
        return [order_by_gender(ascending)]
    elif order_by == 'date_of_birth':
        return order_by_date_of_birth(user, ascending)
    else:
        return [order_by_radar_id(ascending)]

def get_patients_for_user_query(user, params=None):
    # True if the query is filtering on demographics
    filter_by_demographics = False

    query = db_session.query(Patient)

    if params is not None:
        query, filter_by_demographics = filter_patients(user, query, params)

    unit_permission_filter = filter_by_unit_permissions(user)

    if filter_by_demographics:
        permission_filter = unit_permission_filter
    else:
        disease_group_filter = filter_by_disease_group_permissions(user)
        permission_filter = or_(unit_permission_filter, disease_group_filter)

    query = query.filter(permission_filter)

    order_by = params.get('order_by')
    ascending = params.get('order_direction', 'asc') == 'asc'

    order_by = 'date_of_birth'

    query = query.order_by(*order_patients(user, order_by, ascending))

    return query