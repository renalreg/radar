from radar.lib.models import DIAGNOSIS_BIOPSY_DIAGNOSES, DIAGNOSIS_KARYOTYPES
from radar.lib.validation.cohorts import CohortValidationMixin
from radar.lib.validation.core import Field, Validation
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.patients import PatientValidationMixin
from radar.lib.validation.validators import required, optional, \
    valid_date_for_patient, max_length, none_if_blank, in_


class DiagnosisValidation(PatientValidationMixin, CohortValidationMixin, MetaValidationMixin, Validation):
    date = Field([required(), valid_date_for_patient()])
    cohort_diagnosis = Field([required()])
    diagnosis_text = Field([none_if_blank(), optional(), max_length(1000)])
    biopsy_diagnosis = Field([optional(), in_(DIAGNOSIS_BIOPSY_DIAGNOSES.keys())])
    karyotype = Field([optional(), in_(DIAGNOSIS_KARYOTYPES.keys())])


class CohortDiagnosisValidation(CohortValidationMixin, Validation):
    label = Field([required()])
