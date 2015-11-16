from radar.features import FEATURES
from radar.validation.core import Validation, Field
from radar.validation.validators import required, in_


# TODO
class CohortFeatureValidation(Validation):
    name = Field([required(), in_(FEATURES)])
