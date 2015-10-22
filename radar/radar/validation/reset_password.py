from radar.validation.core import Field, Validation
from radar.validation.validators import required


class ResetPasswordValidation(Validation):
    token = Field([required()])
    username = Field([required()])
    password = Field([required()])
