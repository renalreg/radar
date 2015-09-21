from radar.lib.features import FEATURES
from radar.lib.validation.core import Validation, Field


# TODO
from radar.lib.validation.validators import required, in_


class CohortFeatureValidation(Validation):
    name = Field([required(), in_(FEATURES)])
