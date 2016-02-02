from radar.validation.core import Field, Validation, ValidationError
from radar.validation.validators import required
from radar.auth.passwords import check_password_strength, WeakPasswordError


class ResetPasswordValidation(Validation):
    token = Field([required()])
    username = Field([required()])
    password = Field([required()])

    def validate_password(self, password):
        try:
            # TODO pass user argument to check_password_strength
            check_password_strength(password)
        except WeakPasswordError as e:
            raise ValidationError(e.message)

        return password
