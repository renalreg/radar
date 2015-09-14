from radar.lib.models import TRANSPLANT_TYPES
from radar.lib.validation.core import Validation, Field, pass_new_obj, ValidationError
from radar.lib.validation.data_sources import DataSourceValidationMixin
from radar.lib.validation.patients import PatientValidationMixin
from radar.lib.validation.validators import required, valid_date_for_patient, optional, in_


class TransplantValidation(PatientValidationMixin, DataSourceValidationMixin, Validation):
    transplant_date = Field(chain=[required(), valid_date_for_patient()])
    transplant_type = Field(chain=[required(), in_(TRANSPLANT_TYPES.keys())])
    date_failed = Field(chain=[optional(), valid_date_for_patient()])

    @pass_new_obj
    def validate_date_failed(self, obj, date_failed):
        if date_failed < obj.transplant_date:
            raise ValidationError('Must be on or after transplant date.')

        return date_failed
