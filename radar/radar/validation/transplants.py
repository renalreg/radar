from radar.models.transplants import TYPES_OF_TRANSPLANT
from radar.validation.core import Validation, Field, pass_new_obj, ValidationError, ListField
from radar.validation.data_sources import DataSourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, valid_date_for_patient, optional, in_


class TransplantRejectionValidation(Validation):
    # TODO after date_of_transplant
    date_of_rejection = Field([required(), valid_date_for_patient()])


class TransplantBiopsyValidation(Validation):
    # TODO after date_of_transplant
    date_of_biopsy = Field([required(), valid_date_for_patient()])
    recurrence = Field([optional()])


class TransplantValidation(PatientValidationMixin, DataSourceValidationMixin, MetaValidationMixin, Validation):
    date_of_transplant = Field([required(), valid_date_for_patient()])
    type_of_transplant = Field([required(), in_(TYPES_OF_TRANSPLANT.keys())])
    date_of_failure = Field([optional(), valid_date_for_patient()])
    rejections = ListField(TransplantRejectionValidation())
    biopsies = ListField(TransplantBiopsyValidation())

    @pass_new_obj
    def validate_date_of_failure(self, obj, date_of_failure):
        if date_of_failure < obj.date_of_transplant:
            raise ValidationError('Must be on or after transplant date.')

        return date_of_failure
