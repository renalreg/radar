from radar.validation.core import Field, Validation
from radar.validation.validators import required


class ForgotPasswordValidation(Validation):
    username = Field([required()])
