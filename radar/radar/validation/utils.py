from radar.models import User, Post, PatientDemographics, Dialysis, Medication, Patient, Transplant, Hospitalisation, \
    Plasmapheresis, RenalImaging, Cohort, Organisation, OrganisationPatient, OrganisationUser, CohortPatient, CohortUser, \
    DataSource, ResultGroup, PatientAlias, PatientNumber, PatientAddress, Disorder, CohortDiagnosis, ResultSpec, \
    ResultGroupSpec, ResultGroupResultSpec, CohortFeature, CohortResultGroupSpec
from radar.models.consultants import Consultant
from radar.validation.cohort_features import CohortFeatureValidation
from radar.validation.cohort_patients import CohortPatientValidation
from radar.validation.cohort_result_group_specs import CohortResultGroupSpecValidation
from radar.validation.cohort_users import CohortUserValidation
from radar.validation.cohorts import CohortValidation
from radar.validation.comorbidities import DisorderValidation
from radar.validation.data_sources import DataSourceValidation
from radar.validation.diagnoses import CohortDiagnosisValidation
from radar.validation.dialysis import DialysisValidation
from radar.validation.hospitalisations import HospitalisationValidation
from radar.validation.medications import MedicationValidation
from radar.validation.organisation_patients import OrganisationPatientValidation
from radar.validation.organisation_users import OrganisationUserValidation
from radar.validation.organisations import OrganisationValidation
from radar.validation.patient_addresses import PatientAddressValidation
from radar.validation.patient_aliases import PatientAliasValidation
from radar.validation.patient_demographics import PatientDemographicsValidation
from radar.validation.patient_numbers import PatientNumberValidation
from radar.validation.patients import PatientValidation
from radar.validation.plasmapheresis import PlasmapheresisValidation
from radar.validation.posts import PostValidation
from radar.validation.renal_imaging import RenalImagingValidation
from radar.validation.result_group_result_specs import ResultGroupResultSpecValidation
from radar.validation.result_group_specs import ResultGroupSpecValidation
from radar.validation.result_specs import ResultSpecValidation
from radar.validation.result_groups import ResultGroupValidation
from radar.validation.transplants import TransplantValidation
from radar.validation.users import UserValidation
from radar.validation.consultants import ConsultantValidation
from radar.database import db
from radar.auth.sessions import current_user

VALIDATIONS = {
    User: UserValidation,
    Post: PostValidation,
    ResultGroup: ResultGroupValidation,
    DataSource: DataSourceValidation,
    Cohort: CohortValidation,
    Organisation: OrganisationValidation,
    OrganisationUser: OrganisationUserValidation,
    OrganisationPatient: OrganisationPatientValidation,
    CohortUser: CohortUserValidation,
    CohortPatient: CohortPatientValidation,
    RenalImaging: RenalImagingValidation,
    Plasmapheresis: PlasmapheresisValidation,
    Hospitalisation: HospitalisationValidation,
    Transplant: TransplantValidation,
    Patient: PatientValidation,
    Medication: MedicationValidation,
    Dialysis: DialysisValidation,
    PatientDemographics: PatientDemographicsValidation,
    PatientAlias: PatientAliasValidation,
    PatientNumber: PatientNumberValidation,
    PatientAddress: PatientAddressValidation,
    Disorder: DisorderValidation,
    CohortDiagnosis: CohortDiagnosisValidation,
    ResultSpec: ResultSpecValidation,
    ResultGroupSpec: ResultGroupSpecValidation,
    ResultGroupResultSpec: ResultGroupResultSpecValidation,
    CohortFeature: CohortFeatureValidation,
    CohortResultGroupSpec: CohortResultGroupSpecValidation,
    Consultant: ConsultantValidation,
}


def validate(obj, old_obj=None, ctx=None):
    model_class = obj.__class__
    validation_class = VALIDATIONS[model_class]
    validation = validation_class()

    if old_obj is None:
        old_obj = model_class()

    if ctx is None:
        ctx = {}

    if ctx.get('user') is None:
        ctx['user'] = current_user

    with db.session.no_autoflush:
        validation.before_update(ctx, old_obj)
        old_obj = validation.clone(old_obj)
        obj = validation.after_update(ctx, old_obj, obj)

    return obj
