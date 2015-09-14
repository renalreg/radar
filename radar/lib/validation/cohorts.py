from radar.lib.validation.core import Field
from radar.lib.validation.validators import required


class CohortValidationMixin(object):
    cohort = Field(chain=[required()])
