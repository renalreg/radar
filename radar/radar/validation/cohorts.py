from radar.validation.core import Field, Validation
from radar.validation.validators import required, not_empty, none_if_blank, optional, sanitize_html


class CohortValidation(Validation):
    code = Field([not_empty()])
    name = Field([not_empty()])
    short_name = Field([not_empty()])
    notes = Field([none_if_blank(), optional(), sanitize_html()])


class CohortValidationMixin(object):
    cohort = Field([required()])
