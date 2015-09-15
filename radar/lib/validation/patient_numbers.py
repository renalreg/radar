from radar.lib.serializers import Field
from radar.lib.validation.core import Validation
from radar.lib.validation.data_sources import DataSourceValidationMixin
from radar.lib.validation.patients import PatientValidationMixin
from radar.lib.validation.validators import required, max_length, not_empty


class PatientNumberValidation(PatientValidationMixin, DataSourceValidationMixin, Validation):
    organisation = Field([required()])
    number = Field([not_empty(), max_length(50)])
