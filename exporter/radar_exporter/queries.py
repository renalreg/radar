from sqlalchemy.orm import aliased
from sqlalchemy import or_, and_

from radar.database import db
from radar.models.patients import Patient
from radar.models.medications import Medication
from radar.models.genetics import Genetics
from radar.models.family_histories import FamilyHistory, FamilyHistoryRelative
from radar.models.patient_demographics import PatientDemographics
from radar.models.patient_aliases import PatientAlias
from radar.models.patient_addresses import PatientAddress
from radar.models.patient_numbers import PatientNumber
from radar.models.diagnoses import PatientDiagnosis
from radar.models.pathology import Pathology
from radar.models.groups import Group, GroupPatient, GroupUser
from radar.models.ins import InsClinicalPicture, InsRelapse
from radar.models.dialysis import Dialysis
from radar.models.plasmapheresis import Plasmapheresis
from radar.models.transplants import Transplant, TransplantRejection, TransplantBiopsy
from radar.models.hospitalisations import Hospitalisation
from radar.roles import PERMISSION, get_roles_with_permission
from radar.models.groups import GROUP_TYPE
from radar.models.renal_progressions import RenalProgression


class FilterRegistry(object):
    def __init__(self):
        self.filters = {}

    def register(self, klass, f):
        self.filters[klass] = f

    def filter_objects(self, klass, user=None, query=None):
        if query is None:
            query = db.session.query(klass)

        query = self.filters[klass](klass, query, user)

        return query


registry = FilterRegistry()


def filter_by_patient(query, user, patient_id, demographics=False):
    if demographics:
        permission = PERMISSION.VIEW_DEMOGRAPHICS
    else:
        permission = PERMISSION.VIEW_PATIENT

    if not user.is_admin:
        roles = get_roles_with_permission(permission)
        patient_alias = aliased(Patient)
        sub_query = db.session.query(patient_alias)\
            .join(patient_alias.group_patients)\
            .join(GroupPatient.group)\
            .join(Group.group_users)\
            .filter(
                patient_alias.id == patient_id,
                GroupUser.user_id == user.id,
                GroupUser.role.in_(roles)
            )

        query = query.filter(sub_query.exists())

    return query


def filter_by_group(query, user, patient_id, group_id):
    # Filter the query based on the user's group membership
    # Admins can view all data so don't filter their queries
    if not user.is_admin:
        group_a = aliased(Group)
        group_b = aliased(Group)

        # Check if the user has permission through their group membership (requires the VIEW_PATIENT permission)
        # If the user has the VIEW_PATIENT permission on one of the patient's hospitals they can view all cohort data
        sub_query = db.session.query(Group)\
            .join(group_b, GroupPatient.group)\
            .join(Group.group_users)\
            .filter(
                GroupPatient.patient_id == patient_id,
                GroupUser.user == user,
                GroupUser.role.in_(get_roles_with_permission(PERMISSION.VIEW_PATIENT)),
                or_(
                    GroupPatient.group_id == group_id,
                    and_(
                        group_a.type == GROUP_TYPE.COHORT,
                        group_b.type == GROUP_TYPE.HOSPITAL
                    )
                )
            )\
            .exists()

        # Filter the query to only include rows the user has permission to see
        query = query.filter(sub_query)

    return query


def patient_helper(klass):
    def f(user):
        q = db.session.query(klass)
        q = filter_by_patient(q, user, klass.patient_id)
        return q

    return f


def patient_group_helper(klass):
    def f(user):
        q = db.session.query(klass)
        q = filter_by_group(q, user, klass.patient_id, klass.group_id)
        return q

    return f


def patient_demographics_helper(klass):
    def f(user):
        q = db.session.query(klass)
        q = filter_by_patient(q, user, klass.patient_id, demographics=True)
        return q

    return f


def get_patients(user):
    q = db.session.query(Patient)
    q = filter_by_patient(q, user, Patient.id)
    return q


def get_family_history_relatives(user):
    q = db.session.query(FamilyHistoryRelative)
    q = q.join(FamilyHistoryRelative.family_history)
    q = filter_by_group(q, user, FamilyHistory.patient_id, FamilyHistory.group_id)
    return q


def get_transplant_biopsies(user):
    q = db.session.query(TransplantBiopsy)
    q = q.join(TransplantBiopsy.transplant)
    q = filter_by_group(q, user, Transplant.patient_id, Transplant.group_id)
    return q


def get_transplant_rejections(user):
    q = db.session.query(TransplantRejection)
    q = q.join(TransplantRejection.transplant)
    q = filter_by_group(q, user, Transplant.patient_id, Transplant.group_id)
    return q


get_patient_demographics = patient_helper(PatientDemographics)
get_patient_aliases = patient_demographics_helper(PatientAlias)
get_patient_addresses = patient_helper(PatientAddress)
get_patient_numbers = patient_demographics_helper(PatientNumber)
get_medications = patient_helper(Medication)
get_patient_diagnoses = patient_helper(PatientDiagnosis)
get_family_histories = patient_group_helper(FamilyHistory)
get_genetics = patient_group_helper(Genetics)
get_pathology = patient_helper(Pathology)
get_ins_clinical_pictures = patient_helper(InsClinicalPicture)
get_ins_relapses = patient_helper(InsRelapse)
get_dialyses = patient_helper(Dialysis)
get_plasmapheresis = patient_helper(Plasmapheresis)
get_transplants = patient_helper(Transplant)
get_hospitalisations = patient_helper(Hospitalisation)
get_group_patients = patient_helper(GroupPatient)
get_renal_progressions = patient_helper(RenalProgression)
