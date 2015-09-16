from radar.lib.roles import ORGANISATION_ROLES
from radar.lib.validation.core import Validation, Field
from radar.lib.validation.meta import MetaValidationMixin
from radar.lib.validation.validators import required, in_


# TODO
class OrganisationUserValidation(MetaValidationMixin, Validation):
    organisation = Field([required()])
    user = Field([required()])
    role = Field([required(), in_(ORGANISATION_ROLES.keys())])
