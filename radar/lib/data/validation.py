from radar.lib.models import User, Post, PatientDemographics, Dialysis, Medication, Patient, Transplant, Hospitalisation, \
    Plasmapheresis, RenalImaging, Cohort, Organisation, OrganisationPatient, OrganisationUser, CohortPatient, CohortUser, \
    DataSource, ResultGroup
from radar.lib.validation.cohort_patients import CohortPatientValidation
from radar.lib.validation.cohort_users import CohortUserValidation
from radar.lib.validation.cohorts import CohortValidation
from radar.lib.validation.data_sources import DataSourceValidation
from radar.lib.validation.dialysis import DialysisValidation
from radar.lib.validation.hospitalisations import HospitalisationValidation
from radar.lib.validation.medications import MedicationValidation
from radar.lib.validation.organisation_patients import OrganisationPatientValidation
from radar.lib.validation.organisation_users import OrganisationUserValidation
from radar.lib.validation.organisations import OrganisationValidation
from radar.lib.validation.patient_demographics import PatientDemographicsValidation
from radar.lib.validation.patients import PatientValidation
from radar.lib.validation.plasmapheresis import PlasmapheresisValidation
from radar.lib.validation.posts import PostValidation
from radar.lib.validation.renal_imaging import RenalImagingValidation
from radar.lib.validation.result_groups import ResultGroupValidation
from radar.lib.validation.transplants import TransplantValidation
from radar.lib.validation.users import UserValidation


def validate_user(obj):
    return validate(User, UserValidation, obj)


def validate_post(obj):
    return validate(Post, PostValidation, obj)


def validate_patient_demographics(obj):
    return validate(PatientDemographics, PatientDemographicsValidation, obj)


def validate_dialysis(obj):
    return validate(Dialysis, DialysisValidation, obj)


def validate_medication(obj):
    return validate(Medication, MedicationValidation, obj)


def validate_patient(obj):
    return validate(Patient, PatientValidation, obj)


def validate_transplant(obj):
    return validate(Transplant, TransplantValidation, obj)


def validate_hospitalisation(obj):
    return validate(Hospitalisation, HospitalisationValidation, obj)


def validate_plasmapheresis(obj):
    return validate(Plasmapheresis, PlasmapheresisValidation, obj)


def validate_renal_imaging(obj):
    return validate(RenalImaging, RenalImagingValidation, obj)


def validate_cohort_patient(obj):
    return validate(CohortPatient, CohortPatientValidation, obj)


def validate_cohort_user(obj):
    return validate(CohortUser, CohortUserValidation, obj)


def validate_organisation_patient(obj):
    return validate(OrganisationPatient, OrganisationPatientValidation, obj)


def validate_organisation_user(obj):
    return validate(OrganisationUser, OrganisationUserValidation, obj)


def validate_organisation(obj):
    return validate(Organisation, OrganisationValidation, obj)


def validate_cohort(obj):
    return validate(Cohort, CohortValidation, obj)


def validate_data_source(obj):
    return validate(DataSource, DataSourceValidation, obj)


def validate_result_group(obj):
    return validate(ResultGroup, ResultGroupValidation, obj)


def validate(model_class, validation_class, obj):
    validation = validation_class()
    ctx = {'user': User.query.filter(User.username == 'admin').one()}
    validation.before_update(ctx, model_class())
    old_obj = validation.clone(obj)
    obj = validation.after_update(ctx, old_obj, obj)
    return obj
