from radar.validation.core import Validation, Field
from radar.validation.sources import RadarSourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import max_length, not_empty, normalise_whitespace, upper


class PatientAliasValidation(PatientValidationMixin, RadarSourceValidationMixin, MetaValidationMixin, Validation):
    first_name = Field([not_empty(), normalise_whitespace(), upper(), max_length(100)])
    last_name = Field([not_empty(), normalise_whitespace(), upper(), max_length(100)])
