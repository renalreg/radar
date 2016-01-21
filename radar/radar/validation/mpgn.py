from radar.validation.core import Validation, Field
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import optional, required, valid_date_for_patient, \
    max_length, none_if_blank
from radar.validation.meta import MetaValidationMixin


class MpgnClinicalPictureValidation(PatientValidationMixin, MetaValidationMixin, Validation):
    date_of_picture = Field([required(), valid_date_for_patient()])
    oedema = Field([optional()])
    hypertension = Field([optional()])
    urticaria = Field([optional()])
    partial_lipodystrophy = Field([optional()])
    infection = Field([optional()])
    infection_details = Field([none_if_blank(), optional(), max_length(10000)])
    ophthalmoscopy = Field([optional()])
    ophthalmoscopy_details = Field([none_if_blank(), optional(), max_length(10000)])
    comments = Field([none_if_blank(), optional(), max_length(5000)])

    def pre_validate(self, obj):
        # Remove infection details if the patient didn't have an infection
        if not obj.infection:
            obj.infection_details = None

        # Remove ophthalmoscopy details if a ophthalmoscopy test wan't performed
        if not obj.ophthalmoscopy:
            obj.ophthalmoscopy_details = None

        return obj
