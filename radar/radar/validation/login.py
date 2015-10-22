from radar.validation.core import Field, Validation
from radar.validation.validators import required, optional


class LoginValidation(Validation):
    username = Field([required()])
    password = Field([required()])
    logout_other_sessions = Field([optional()])
