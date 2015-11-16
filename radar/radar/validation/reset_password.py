from radar.validation.core import Field, Validation, ValidationError
from radar.validation.validators import required
from radar.auth.passwords import is_strong_password


class ResetPasswordValidation(Validation):
    token = Field([required()])
    username = Field([required()])
    password = Field([required()])

    def validate_password(self, password):
        # TODO second argument
        if not is_strong_password(password):
            raise ValidationError('Password is too weak.')

        return password
