from radar.validation.core import Field, Validation
from radar.validation.validators import required


class ForgotUsernameValidation(Validation):
    email = Field([required()])
