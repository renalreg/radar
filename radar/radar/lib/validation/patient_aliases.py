from radar.lib.validation.core import Validation, Field
from radar.lib.validation.data_sources import RadarDataSourceValidationMixin
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.patients import PatientValidationMixin
from radar.lib.validation.validators import max_length, not_empty, normalise_whitespace, upper


class PatientAliasValidation(PatientValidationMixin, RadarDataSourceValidationMixin, MetaValidationMixin, Validation):
    first_name = Field([not_empty(), normalise_whitespace(), upper(), max_length(100)])
    last_name = Field([not_empty(), normalise_whitespace(), upper(), max_length(100)])
