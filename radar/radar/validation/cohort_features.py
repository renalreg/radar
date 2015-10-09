from radar.features import FEATURES
from radar.validation.core import Validation, Field


# TODO
from radar.validation.validators import required, in_


class CohortFeatureValidation(Validation):
    name = Field([required(), in_(FEATURES)])
