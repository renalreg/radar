from radar.lib.serializers import Field
from radar.lib.validation.core import Validation
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.validators import required


# TODO
class OrganisationUserValidation(MetaValidationMixin, Validation):
    cohort = Field([required()])
    user = Field([required()])
