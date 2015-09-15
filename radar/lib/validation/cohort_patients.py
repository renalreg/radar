from radar.lib.serializers import Field
from radar.lib.validation.core import Validation
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.validators import required


# TODO
class CohortPatientValidation(MetaValidationMixin, Validation):
    cohort = Field([required()])
    patient = Field([required()])
