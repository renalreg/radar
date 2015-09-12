from radar.lib.validation.core import Field, Validation, ValidationError, pass_call, pass_new_obj
from radar.lib.validation.data_sources import DataSourceValidationMixin
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.patients import PatientValidationMixin
from radar.lib.validation.validators import after_date_of_birth, not_in_future, required, optional


class DialysisValidation(PatientValidationMixin, DataSourceValidationMixin, MetaValidationMixin, Validation):
    from_date = Field(chain=[required(), after_date_of_birth(), not_in_future()])
    to_date = Field(chain=[optional(), after_date_of_birth(), not_in_future()])
    dialysis_type = Field(chain=[required()])
    patient = Field(chain=[required()])

    @pass_new_obj
    def validate_to_date(self, obj, to_date):
        if to_date < obj.from_date:
            raise ValidationError('Must be on or after from date.')
