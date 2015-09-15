from radar.lib.validation.core import Validation, Field
from radar.lib.validation.meta import MetaValidationMixin


# TODO
class UserValidation(MetaValidationMixin, Validation):
    id = Field()
    username = Field()
    password = Field()
    email = Field()
    first_name = Field()
    last_name = Field()
    is_admin = Field()
