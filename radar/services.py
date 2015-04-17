from sqlalchemy import or_
from sqlalchemy.orm import aliased

from radar.database import db_session
from radar.models import Patient, UnitPatient, Unit, UnitUser, DiseaseGroupPatient, DiseaseGroup, DiseaseGroupUser

def get_patients_for_user(user, search=None):
    # True if this query requires unit permissions (i.e. querying for demographics)
    requires_unit_permissions = False

    query = db_session.query(Patient)

    if search is not None:
        if search.get('first_name'):
            requires_unit_permissions = True
            query = query.filter(Patient.first_name.like('%' + search.get('first_name') + '%'))

        if search.get('last_name'):
            requires_unit_permissions = True
            query = query.filter(Patient.last_name.like('%' + search.get('last_name') + '%'))

        # Filter by unit
        if search.get('unit_id'):
            unit = Unit.query.get(search.get('unit_id'))

            # Unit exists
            if unit is not None:
                # User belongs to unit
                if is_user_in_unit(user, unit):
                    requires_unit_permissions = True
                    query = query.join(UnitPatient).filter(UnitPatient.unit == unit)

        # Filter by disease group
        if search.get('disease_group_id'):
            # Get the disease group with this id
            disease_group = DiseaseGroup.query.get(search.get('disease_group_id'))

            # Disease group exists
            if disease_group is not None:
                # If the user doesn't belong to the disease group they need unit permissions
                if not is_user_in_disease_group(user, disease_group):
                    requires_unit_permissions = True

                # Filter by disease group
                query = query.join(DiseaseGroupPatient).filter(DiseaseGroupPatient.disease_group == disease_group)

    patient_unit_alias = aliased(Patient)
    permission_through_unit = db_session.query(patient_unit_alias)\
        .join(patient_unit_alias.units)\
        .join(UnitPatient.unit)\
        .join(Unit.users)\
        .filter(UnitUser.user_id == user.id, patient_unit_alias.id == Patient.id)\
        .exists()

    if requires_unit_permissions:
        permission_filter = permission_through_unit
    else:
        patient_disease_group_alias = aliased(Patient)
        permission_through_disease_group = db_session.query(patient_disease_group_alias)\
            .join(patient_disease_group_alias.disease_groups)\
            .join(DiseaseGroupPatient.disease_group)\
            .join(DiseaseGroup.users)\
            .filter(DiseaseGroupUser.user_id == user.id, patient_disease_group_alias.id == Patient.id)\
            .exists()

        permission_filter = or_(permission_through_unit, permission_through_disease_group)

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