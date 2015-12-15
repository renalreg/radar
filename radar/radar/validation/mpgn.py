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
    recent_infection = Field([optional()])
    recent_infection_details = Field([none_if_blank(), optional(), max_length(1000)])
    ophthalmoscopy = Field([optional()])
    ophthalmoscopy_details = Field([none_if_blank(), optional(), max_length(1000)])
    comments = Field([none_if_blank(), optional(), max_length(5000)])

    def pre_validate(self, obj):
        # Remove recent infection details if the patient didn't have a recent infection
        if not obj.recent_infection:
            obj.recent_infection_details = None

        # Remove ophthalmoscopy details if a ophthalmoscopy test wan't performed
        if not obj.ophthalmoscopy:
            obj.ophthalmoscopy_details = None

        return obj
