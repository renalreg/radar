from radar.lib.roles import COHORT_ROLES
from radar.lib.validation.core import Validation, Field
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.validators import required, in_


# TODO
class CohortUserValidation(MetaValidationMixin, Validation):
    cohort = Field([required()])
    user = Field([required()])
    role = Field([required(), in_(COHORT_ROLES.keys())])
