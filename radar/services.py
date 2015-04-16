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

        if search.get('unit_id'):
            unit_user = UnitUser.query.filter(UnitUser.unit_id == search.get('unit_id'), UnitUser.user == user)

            # User has permission to filter by this unit
            if unit_user is not None:
                # TODO
                pass

        if search.get('disease_group_id'):
            # TODO more complicated than this
            dg_user = DiseaseGroupUser.query.filter(
                DiseaseGroupUser.disease_group_id == search.get('disease_group_id'),
                DiseaseGroupUser.user == user
            )

            # User has permission to filter by this disease group
            if dg_user is not None:
                # TODO
                pass

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

def get_units_for_user(user):
    return db_session.query(Unit)\
        .join(Unit.users)\
        .filter(UnitUser.user == user)\
        .all()

def get_disease_groups_for_user(user):
    return db_session.query(DiseaseGroup)\
        .join(DiseaseGroup.users)\
        .filter(DiseaseGroupUser.user == user)\
        .all()