from radar.auth.passwords import check_password_hash
from radar.validation.core import Validation, Field, pass_old_obj, pass_old_value, pass_new_value, \
    pass_context, ValidationError
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import required, optional, email_address


class PasswordField(Field):
    def set_value(self, obj, value):
        if value is not None:
            super(PasswordField, self).set_value(obj, value)


class PasswordHashField(Field):
    def set_value(self, obj, value):
        pass


# TODO
# TODO check username not already taken
class UserValidation(MetaValidationMixin, Validation):
    id = Field()
    username = Field([required()])
    password = PasswordField([optional()])
    password_hash = PasswordHashField([optional()])
    email = Field([required(), email_address()])
    first_name = Field([required()])
    last_name = Field([required()])
    is_admin = Field([required()])

    @pass_context
    @pass_old_obj
    def validate(self, ctx, old_obj, new_obj):
        password_required = False

        # Email changed for existing user
        if old_obj.id is not None and old_obj.email != new_obj.email:
            password_required = True

        # Password changed for existing user
        if old_obj.id is not None and old_obj.password_hash != new_obj.password_hash:
            password_required = True

        if password_required:
            current_password_hash = old_obj.password_hash
            current_password = ctx.get('current_password')

            if current_password is None or not check_password_hash(current_password_hash, current_password):
                raise ValidationError({'current_password': 'Incorrect password!'})

        return new_obj
