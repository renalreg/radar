from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import true

from radar.database import db
from radar.models.codes import Code
from radar.models.consultants import Consultant, GroupConsultant
from radar.models.diagnoses import Diagnosis, DiagnosisCode, GroupDiagnosis, PatientDiagnosis
from radar.models.dialysis import Dialysis
from radar.models.family_histories import FamilyHistory, FamilyHistoryRelative
from radar.models.fetal_ultrasounds import FetalUltrasound
from radar.models.forms import Entry
from radar.models.genetics import Genetics
from radar.models.groups import Group, GROUP_TYPE, GroupPatient, GroupUser
from radar.models.hospitalisations import Hospitalisation
from radar.models.ins import InsClinicalPicture, InsRelapse
from radar.models.medications import Medication
from radar.models.mpgn import MpgnClinicalPicture
from radar.models.nephrectomies import Nephrectomy
from radar.models.nurture_tubes import Samples
from radar.models.pathology import Pathology
from radar.models.patient_addresses import PatientAddress
from radar.models.patient_aliases import PatientAlias
from radar.models.patient_demographics import PatientDemographics
from radar.models.patient_numbers import PatientNumber
from radar.models.patients import Patient
from radar.models.pkd import LiverDiseases, LiverImaging, LiverTransplant, Nutrition
from radar.models.plasmapheresis import Plasmapheresis
from radar.models.pregnancies import Pregnancy
from radar.models.renal_imaging import RenalImaging
from radar.models.renal_progressions import RenalProgression
from radar.models.results import Result
from radar.models.salt_wasting import SaltWastingClinicalFeatures
from radar.models.transplants import Transplant, TransplantBiopsy, TransplantRejection
from radar.roles import get_roles_with_permission, PERMISSION


def filter_by_patient_permissions(query, user, patient_id, demographics=False):
    if demographics:
        permission = PERMISSION.VIEW_DEMOGRAPHICS
    else:
        permission = PERMISSION.VIEW_PATIENT

    if not user.is_admin:
        roles = get_roles_with_permission(permission)
        patient_alias = aliased(Patient)
        sub_query = db.session.query(patient_alias)
        sub_query = sub_query.join(patient_alias.group_patients)
        sub_query = sub_query.join(GroupPatient.group)
        sub_query = sub_query.join(Group.group_users)
        sub_query = sub_query.filter(
            patient_alias.id == patient_id,
            GroupUser.user_id == user.id,
            GroupUser.role.in_(roles),
        )

        query = query.filter(sub_query.exists())

    return query


def filter_by_patient_group_permissions(query, user, patient_id, group_id):
    # Filter the query based on the user's group membership
    # Admins can view all data so don't filter their queries
    if not user.is_admin:
        group_a = aliased(Group)
        group_b = aliased(Group)

        # Check if the user has permission through their group membership (requires the VIEW_PATIENT permission)
        # If the user has the VIEW_PATIENT permission on one of the patient's hospitals they can view all cohort data
        sub_query = db.session.query(Group)
        sub_query = sub_query.join(group_b, GroupPatient.group)
        sub_query = sub_query.join(Group.group_users)
        sub_query = sub_query.filter(
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
        )
        sub_query = sub_query.exists()

        # Filter the query to only include rows the user has permission to see
        query = query.filter(sub_query)

    return query


def filter_by_patient_group(query, group, patient_id):
    patient_alias = aliased(Patient)
    group_patient_alias = aliased(GroupPatient)

    sub_query = db.session.query(patient_alias)
    sub_query = sub_query.join(group_patient_alias, patient_alias.group_patients)
    sub_query = sub_query.filter(
        group_patient_alias.patient_id == patient_id,
        group_patient_alias.group_id == group.id
    )
    sub_query = sub_query.exists()

    query = query.filter(sub_query)

    return query


def filter_by_data_group(query, group, group_id):
    return query.filter(group_id == group.id)


def patient_helper(klass):
    def f(config):
        q = db.session.query(klass).filter(Patient.test != true(), klass.patient_id == Patient.id)
        q = q.order_by(klass.patient_id, klass.id)
        q = _patient_filter(q, klass.patient_id, config['user'], config['patient_group'])
        return q

    return f


def _patient_filter(query, patient_id, user, patient_group):
    if user is not None:
        query = filter_by_patient_permissions(query, user, patient_id)

    if patient_group is not None:
        query = filter_by_patient_group(query, patient_group, patient_id)

    return query


def patient_group_helper(klass):
    def f(config):
        q = db.session.query(klass).order_by(klass.patient_id, klass.id)
        q = _patient_group_filter(
            q,
            klass.patient_id,
            klass.group_id,
            config['user'],
            config['patient_group'],
            config['data_group'])
        return q

    return f


def _patient_group_filter(query, patient_id, group_id, user, patient_group, data_group):
    if user is not None:
        query = filter_by_patient_group_permissions(query, user, patient_id, group_id)

    if patient_group is not None:
        query = filter_by_patient_group(query, patient_group, patient_id)

    if data_group is not None:
        query = filter_by_data_group(query, data_group, group_id)

    return query


def get_patients(config):
    q = db.session.query(Patient).filter(Patient.test != true()).order_by(Patient.id)
    q = _patient_filter(q, Patient.id, config['user'], config['patient_group'])
    return q


def get_family_history_relatives(config):
    q = db.session.query(FamilyHistoryRelative)
    q = q.join(FamilyHistoryRelative.family_history)
    q = _patient_group_filter(
        q,
        FamilyHistory.patient_id,
        FamilyHistory.group_id,
        config['user'],
        config['patient_group'],
        config['data_group'])
    q = q.order_by(FamilyHistory.patient_id, FamilyHistory.id, FamilyHistoryRelative.id)
    return q


def get_transplant_biopsies(config):
    q = db.session.query(TransplantBiopsy)
    q = q.join(TransplantBiopsy.transplant)
    q = _patient_filter(q, Transplant.patient_id, config['user'], config['patient_group'])
    q = q.order_by(Transplant.patient_id, Transplant.id, TransplantBiopsy.id)
    return q


def get_transplant_rejections(config):
    q = db.session.query(TransplantRejection)
    q = q.join(TransplantRejection.transplant)
    q = _patient_filter(q, Transplant.patient_id, config['user'], config['patient_group'])
    q = q.order_by(Transplant.patient_id, Transplant.id, TransplantRejection.id)
    return q


def get_form_data(config):
    q = db.session.query(Entry)
    q = q.filter(Patient.test != true(), Entry.patient_id == Patient.id)
    q = q.order_by(Entry.patient_id, Entry.id)
    q = _patient_filter(q, Entry.patient_id, config['user'], config['patient_group'])
    q = q.filter(Entry.form.has(slug=config['name']))
    return q


def get_consultants(config):
    q = db.session.query(Consultant)
    q = q.join(Consultant.group_consultants)
    q = q.filter(GroupConsultant.group == config['data_group'])
    return q


def get_patient_diagnoses(config):
    """Join to get EDTA and other system codes in a more efficient way."""
    q = patient_helper(PatientDiagnosis)(config)
    q = q.join(Diagnosis, PatientDiagnosis.diagnosis_id == Diagnosis.id, isouter=True)
    q = q.join(DiagnosisCode, Diagnosis.id == DiagnosisCode.diagnosis_id, isouter=True)
    q = q.join(Code, Code.id == DiagnosisCode.code_id, isouter=True)
    return q


def get_primary_diagnoses(config):
    """Return query to get primary diagnoses for data_group."""
    q = db.session.query(Diagnosis).filter(GroupDiagnosis.group == config['data_group'])
    q = q.join(GroupDiagnosis, GroupDiagnosis.diagnosis_id == Diagnosis.id)
    return q


get_patient_demographics = patient_helper(PatientDemographics)
get_patient_aliases = patient_helper(PatientAlias)
get_patient_addresses = patient_helper(PatientAddress)
get_patient_numbers = patient_helper(PatientNumber)
get_medications = patient_helper(Medication)
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
get_renal_imaging = patient_helper(RenalImaging)
get_renal_progressions = patient_helper(RenalProgression)
get_mpgn_clinical_pictures = patient_helper(MpgnClinicalPicture)
get_results = patient_helper(Result)
get_pregnancies = patient_helper(Pregnancy)
get_fetal_ultrasounds = patient_helper(FetalUltrasound)
get_clinical_features = patient_helper(SaltWastingClinicalFeatures)
get_liver_imaging = patient_helper(LiverImaging)
get_liver_diseases = patient_helper(LiverDiseases)
get_liver_transplants = patient_helper(LiverTransplant)
get_nephrectomies = patient_helper(Nephrectomy)
get_nutrition = patient_helper(Nutrition)
get_nurture_samples = patient_helper(Samples)
