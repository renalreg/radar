from radar.validation.core import Validation, Field
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, valid_date_for_patient, in_, optional
from radar.models.alport import DEAFNESS_OPTIONS, DEAFNESS_NO
from radar.validation.meta import MetaValidationMixin


class AlportClinicalPictureValidation(PatientValidationMixin, MetaValidationMixin, Validation):
    date_of_picture = Field([required(), valid_date_for_patient()])
    deafness = Field([required(), in_(DEAFNESS_OPTIONS.keys())])
    deafness_date = Field([optional(), valid_date_for_patient()])
    hearing_aid_date = Field([optional(), valid_date_for_patient()])

    def pre_validate(self, obj):
        # Patient not deaf
        if obj.deafness == DEAFNESS_NO:
            obj.deafness_date = None
            obj.hearing_aid_date = None

        return obj
