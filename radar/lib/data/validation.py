from radar.lib.models import User, Post, PatientDemographics, Dialysis, Medication, Patient, Transplant, Hospitalisation, \
    Plasmapheresis, RenalImaging, Cohort, Organisation, OrganisationPatient, OrganisationUser, CohortPatient, CohortUser, \
    DataSource, ResultGroup, PatientAlias, PatientNumber, PatientAddress, Disorder, CohortDiagnosis, ResultSpec, \
    ResultGroupSpec, Result, ResultGroupResultSpec, CohortFeature, CohortResultGroupSpec
from radar.lib.validation.cohort_features import CohortFeatureValidation
from radar.lib.validation.cohort_patients import CohortPatientValidation
from radar.lib.validation.cohort_result_group_specs import CohortResultGroupSpecValidation
from radar.lib.validation.cohort_users import CohortUserValidation
from radar.lib.validation.cohorts import CohortValidation
from radar.lib.validation.comorbidities import DisorderValidation
from radar.lib.validation.data_sources import DataSourceValidation
from radar.lib.validation.diagnoses import CohortDiagnosisValidation
from radar.lib.validation.dialysis import DialysisValidation
from radar.lib.validation.hospitalisations import HospitalisationValidation
from radar.lib.validation.medications import MedicationValidation
from radar.lib.validation.organisation_patients import OrganisationPatientValidation
from radar.lib.validation.organisation_users import OrganisationUserValidation
from radar.lib.validation.organisations import OrganisationValidation
from radar.lib.validation.patient_addresses import PatientAddressValidation
from radar.lib.validation.patient_aliases import PatientAliasValidation
from radar.lib.validation.patient_demographics import PatientDemographicsValidation
from radar.lib.validation.patient_numbers import PatientNumberValidation
from radar.lib.validation.patients import PatientValidation
from radar.lib.validation.plasmapheresis import PlasmapheresisValidation
from radar.lib.validation.posts import PostValidation
from radar.lib.validation.renal_imaging import RenalImagingValidation
from radar.lib.validation.result_group_result_specs import ResultGroupResultSpecValidation
from radar.lib.validation.result_group_specs import ResultGroupSpecValidation
from radar.lib.validation.result_specs import ResultSpecValidation
from radar.lib.validation.result_groups import ResultGroupValidation
from radar.lib.validation.results import ResultValidation
from radar.lib.validation.transplants import TransplantValidation
from radar.lib.validation.users import UserValidation

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
    Result: ResultValidation,
    ResultGroupResultSpec: ResultGroupResultSpecValidation,
    CohortFeature: CohortFeatureValidation,
    CohortResultGroupSpec: CohortResultGroupSpecValidation,
}


def validate(obj):
    model_class = obj.__class__
    validation_class = VALIDATIONS[model_class]
    return validation_runner(model_class, validation_class, obj)


def validation_runner(model_class, validation_class, obj):
    validation = validation_class()
    ctx = {'user': User.query.filter(User.username == 'bot').one()}
    validation.before_update(ctx, model_class())
    old_obj = validation.clone(obj)
    obj = validation.after_update(ctx, old_obj, obj)
    return obj
