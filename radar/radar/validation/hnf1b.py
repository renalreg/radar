from radar.validation.core import Validation, Field, pass_call
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import optional, required, valid_date_for_patient, in_, none_if_blank, max_length
from radar.models.hnf1b import TYPES_OF_DIABETES, NO_DIABETES
from radar.validation.meta import MetaValidationMixin


class Hnf1bClinicalPictureValidation(PatientValidationMixin, MetaValidationMixin, Validation):
    date_of_picture = Field([required(), valid_date_for_patient()])
    single_kidney = Field([optional()])
    hyperuricemia_gout = Field([optional()])
    genital_malformation = Field([optional()])
    genital_malformation_details = Field([none_if_blank(), optional(), max_length(10000)])
    familial_cystic_disease = Field([optional()])
    hypertension = Field([optional()])
    type_of_diabetes = Field([optional(), in_(TYPES_OF_DIABETES.keys())])
    date_of_diabetes = Field([optional(), valid_date_for_patient()])
    diabetic_nephropathy = Field([optional()])
    diabetic_retinopathy = Field([optional()])
    diabetic_neuropathy = Field([optional()])
    diabetic_pvd = Field([optional()])

    def pre_validate(self, obj):
        if obj.type_of_diabetes is None or obj.type_of_diabetes == NO_DIABETES:
            obj.date_of_diabetes = None
            obj.diabetic_nephropathy = None
            obj.diabetic_retinopathy = None
            obj.diabetic_neuropathy = None
            obj.diabetic_pvd = None

        if not obj.other_malformation:
            obj.other_malformation_details = None

        if not obj.genital_malformation:
            obj.genital_malformation_details = None

        return obj

    @pass_call
    def validate(self, call, obj):
        # Date is required if the patient has diabetes
        if obj.type_of_diabetes is not None and obj.type_of_diabetes != NO_DIABETES:
            call.validators_for_field([required()], obj, self.date_of_diabetes)

        return obj
