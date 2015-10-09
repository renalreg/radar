from radar.validation.core import Validation, Field
from radar.validation.meta import MetaValidationMixin


# TODO
# TODO check username not already taken
class UserValidation(MetaValidationMixin, Validation):
    id = Field()
    username = Field()
    password = Field()
    email = Field()
    first_name = Field()
    last_name = Field()
    is_admin = Field()
