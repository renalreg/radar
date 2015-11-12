from radar.auth.passwords import check_password_hash
from radar.validation.core import Validation, Field, pass_old_obj, pass_context, ValidationError, pass_new_obj, \
    pass_call, pass_context
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import required, optional, email_address, not_empty


class PasswordField(Field):
    def set_value(self, obj, value):
        if value is not None:
            super(PasswordField, self).set_value(obj, value)


class PasswordHashField(Field):
    def set_value(self, obj, value):
        pass


# TODO check username not already taken
class UserValidation(MetaValidationMixin, Validation):
    id = Field()
    username = Field([required()])
    password = PasswordField([optional()])
    password_hash = PasswordHashField([optional()])
    email = Field([optional(), email_address()])
    first_name = Field([optional()])
    last_name = Field([optional()])
    is_admin = Field([required()])
    force_password_change = Field([required()])

    @pass_call
    @pass_new_obj
    def validate_first_name(self, call, obj, first_name):
        if not obj.is_bot:
            first_name = call.validators([not_empty()], first_name)

        return first_name

    @pass_call
    @pass_new_obj
    def validate_last_name(self, call, obj, last_name):
        if not obj.is_bot:
            last_name = call.validators([not_empty()], last_name)

        return last_name

    @pass_call
    @pass_new_obj
    def validate_email(self, call, obj, email):
        if not obj.is_bot:
            email = call.validators([required()], email)

        return email

    @pass_context
    @pass_old_obj
    @pass_new_obj
    def validate_force_password_change(self, ctx, old_obj, new_obj, value):
        current_user = ctx['user']

        if not current_user.is_admin:
            # New user
            if old_obj.id is None:
                if not force_password_change:
                    raise ValidationError('New users must be forced to change their password.')
            else:
                # An ordinary user tried to force a password change
                if not old_obj.force_password_change and new_obj.force_password_change:
                    raise ValidationError('Only admins can force a password change.')
                elif (
                    old_obj.force_password_change and
                    not new_obj.force_password_change and
                    old_obj.password_hash == new_obj.password_hash
                ):
                    raise ValidationError('A password change is required.')

        return value

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
                # Incorrect password
                raise ValidationError({'current_password': 'Incorrect password!'})
            elif old_obj.force_password_change and new_obj.check_password(current_password):
                # New password must be different to old password if force password change was set
                raise ValidationError({'password': 'New password must be different to old password.'})

        return new_obj
