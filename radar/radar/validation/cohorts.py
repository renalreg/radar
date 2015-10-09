from radar.validation.core import Field, Validation
from radar.validation.validators import required


# TODO
class CohortValidation(Validation):
    pass


class CohortValidationMixin(object):
    cohort = Field([required()])
