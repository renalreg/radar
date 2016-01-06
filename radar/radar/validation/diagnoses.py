from radar.models import DIAGNOSIS_BIOPSY_DIAGNOSES
from radar.validation.cohorts import CohortValidationMixin
from radar.validation.core import Field, Validation, ValidationError, pass_new_obj
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, optional, \
    valid_date_for_patient, max_length, none_if_blank, in_


class DiagnosisValidation(PatientValidationMixin, CohortValidationMixin, MetaValidationMixin, Validation):
    date_of_onset = Field([required(), valid_date_for_patient()])
    date_of_diagnosis = Field([required(), valid_date_for_patient()])
    cohort_diagnosis = Field([required()])
    diagnosis_text = Field([none_if_blank(), optional(), max_length(10000)])
    biopsy_diagnosis = Field([optional(), in_(DIAGNOSIS_BIOPSY_DIAGNOSES.keys())])

    @pass_new_obj
    def validate_date_of_diagnosis(self, obj, date_of_diagnosis):
        if date_of_diagnosis < obj.date_of_onset:
            raise ValidationError('Must be on or after date of onset.')

        return date_of_diagnosis

    @pass_new_obj
    def validate_cohort_diagnosis(self, obj, cohort_diagnosis):
        if cohort_diagnosis.cohort != obj.cohort:
            raise ValidationError('Not a valid diagnosis for this cohort.')

        return cohort_diagnosis


class CohortDiagnosisValidation(CohortValidationMixin, Validation):
    label = Field([required()])
