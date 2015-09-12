from radar.lib.validation.core import Validation, Field
from radar.lib.validation.data_sources import DataSourceValidationMixin
from radar.lib.validation.patients import PatientValidationMixin
from radar.lib.validation.validators import required, valid_date_for_patient


class TransplantValidation(PatientValidationMixin, DataSourceValidationMixin, Validation):
    transplant_date = Field(chain=[required(), valid_date_for_patient()])
    transplant_type = Field(chain=[required()])
