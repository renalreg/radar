from radar.validation.core import Validation, Field, pass_new_obj, ValidationError
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import optional, required, valid_date_for_patient, \
    max_length, none_if_blank, in_
from radar.models.ins import TYPES_OF_KIDNEY, TYPES_OF_REMISSION
from radar.validation.meta import MetaValidationMixin


class InsClinicalPictureValidation(PatientValidationMixin, MetaValidationMixin, Validation):
    date_of_picture = Field([required(), valid_date_for_patient()])
    oedema = Field([optional()])
    hypovalaemia = Field([optional()])
    fever = Field([optional()])
    thrombosis = Field([optional()])
    peritonitis = Field([optional()])
    pulmonary_odemea = Field([optional()])
    hypertension = Field([optional()])
    rash = Field([optional()])
    rash_details = Field([none_if_blank(), optional(), max_length(1000)])
    possible_immunisation_trigger = Field([optional()])
    ophthalmoscopy = Field([optional()])
    ophthalmoscopy_details = Field([none_if_blank(), optional(), max_length(1000)])
    comments = Field([none_if_blank(), optional(), max_length(1000)])

    def pre_validate(self, obj):
        # Remove rash details of the patient didn't have a rash
        if not obj.rash:
            obj.rash_details = None

        # Remove ophthalmoscopy details if a ophthalmoscopy test wan't performed
        if not obj.ophthalmoscopy:
            obj.ophthalmoscopy_details = None

        return obj


class InsRelapseValidation(PatientValidationMixin, MetaValidationMixin, Validation):
    date_of_relapse = Field([required(), valid_date_for_patient()])
    type_of_kidney = Field([required(), in_(TYPES_OF_KIDNEY)])
    viral_trigger = Field([none_if_blank(), optional(), max_length(1000)])
    immunisation_trigger = Field([none_if_blank(), optional(), max_length(1000)])
    other_trigger = Field([none_if_blank(), optional(), max_length(1000)])
    high_dose_oral_prednisolone = Field([optional()])
    iv_methyl_prednisolone = Field([optional()])
    date_of_remission = Field([optional(), valid_date_for_patient()])
    type_of_remission = Field([optional(), in_(TYPES_OF_REMISSION)])

    def pre_validate(self, obj):
        # Remove remission type if the date of remission is missing
        if not obj.date_of_remission:
            obj.type_of_remission = None

        return obj

    @pass_new_obj
    def validate_date_of_remission(self, obj, date_of_remission):
        if date_of_remission < obj.date_of_relapse:
            raise ValidationError('Must be on or after date of relapse.')

        return date_of_remission
