from radar.validation.core import Validation, Field
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import optional, required, valid_date_for_patient, none_if_blank, max_length
from radar.validation.meta import MetaValidationMixin


class Hnf1bClinicalPictureValidation(PatientValidationMixin, MetaValidationMixin, Validation):
    date_of_picture = Field([required(), valid_date_for_patient()])
    single_kidney = Field([optional()])
    hyperuricemia_gout = Field([optional()])
    genital_malformation = Field([optional()])
    genital_malformation_details = Field([none_if_blank(), optional(), max_length(10000)])
    familial_cystic_disease = Field([optional()])
    hypertension = Field([optional()])
