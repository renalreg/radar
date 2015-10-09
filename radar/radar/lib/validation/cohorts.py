from radar.lib.validation.core import Field, Validation
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.validators import required


# TODO
class CohortValidation(Validation):
    pass


class CohortValidationMixin(object):
    cohort = Field([required()])
