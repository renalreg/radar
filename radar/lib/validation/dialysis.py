from radar.lib.validation.core import Field, Validation, ValidationError, pass_new_obj
from radar.lib.validation.data_sources import DataSourceValidationMixin
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.patients import PatientValidationMixin
from radar.lib.validation.validators import required, optional, \
    valid_date_for_patient


class DialysisValidation(PatientValidationMixin, DataSourceValidationMixin, MetaValidationMixin, Validation):
    from_date = Field(chain=[required(), valid_date_for_patient()])
    to_date = Field(chain=[optional(), valid_date_for_patient()])
    dialysis_type = Field(chain=[required()])

    @pass_new_obj
    def validate_to_date(self, obj, to_date):
        if to_date < obj.from_date:
            raise ValidationError('Must be on or after from date.')

        return to_date
