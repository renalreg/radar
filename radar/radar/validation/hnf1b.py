from radar.validation.core import Validation, Field, pass_call
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import optional, required, valid_date_for_patient, in_, none_if_blank, max_length
from radar.models.hnf1b import TYPES_OF_DIABETES, NO_DIABETES
from radar.validation.meta import MetaValidationMixin


class Hnf1bClinicalPictureValidation(PatientValidationMixin, MetaValidationMixin, Validation):
    date_of_picture = Field([required(), valid_date_for_patient()])
    date_of_renal_disease = Field([optional(), valid_date_for_patient()])
    cysts = Field([optional()])
    stones = Field([optional()])
    single_kidney = Field([optional()])
    other_malformation = Field([optional()])
    other_malformation_details = Field([none_if_blank(), optional(), max_length(1000)])
    hyperuricemia_gout = Field([optional()])
    genital_malformation = Field([optional()])
    genital_malformation_details = Field([none_if_blank(), optional(), max_length(1000)])
    familial_cystic_disease = Field([optional()])
    hypertension = Field([optional()])
    type_of_diabetes = Field([optional(), in_(TYPES_OF_DIABETES.keys())])
    date_of_diabetes = Field([optional(), valid_date_for_patient()])
    diabetic_nephropathy = Field([optional()])
    diabetic_retinopathy = Field([optional()])
    diabetic_neuropathy = Field([optional()])
    diabetic_pvd = Field([optional()])

    @pass_call
    def validate(self, call, obj):
        # Date is required if the patient has diabetes
        if obj.type_of_diabetes is not None and obj.type_of_diabetes != NO_DIABETES:
            call.validators_for_field([required()], obj, self.date_of_diabetes)

        return obj
