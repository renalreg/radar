from radar.validation.patients import PatientValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.core import Validation, Field, ValidationError, pass_new_obj
from radar.validation.validators import required, optional


class PatientConsultantValidation(PatientValidationMixin, MetaValidationMixin, Validation):
    from_date = Field([required()])
    to_date = Field([optional()])
    consultant = Field([required()])

    @pass_new_obj
    def validate_to_date(self, obj, to_date):
        if to_date < obj.from_date:
            raise ValidationError('Must be on or after from date.')

        return to_date
