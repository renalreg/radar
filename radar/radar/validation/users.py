from radar.auth.passwords import check_password_hash, is_strong_password
from radar.validation.core import Validation, Field, pass_old_obj, pass_context, ValidationError, pass_new_obj, \
    pass_call, pass_old_value
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import required, optional, email_address, not_empty, none_if_blank


class PasswordField(Field):
    def set_value(self, obj, value):
        # Password is optional but we don't want to overwrite it with None
        if value is not None:
            super(PasswordField, self).set_value(obj, value)


# TODO check username not already taken
class UserValidation(MetaValidationMixin, Validation):
    id = Field([optional()])
    username = Field([required()])
    password = PasswordField([optional()])
    password_hash = Field([optional()])
    email = Field([none_if_blank(), optional(), email_address()])
    first_name = Field([none_if_blank(), optional()])
    last_name = Field([none_if_blank(), optional()])
    is_admin = Field([required()])
    force_password_change = Field([required()])

    @pass_context
    @pass_old_obj
    @pass_old_value
    def validate_username(self, ctx, old_obj, old_username, new_username):
        current_user = ctx['user']

        if old_obj.id is not None and old_username != new_username and not current_user.is_admin:
            raise ValidationError('Only admins can change usernames.')

        return new_username

    @pass_context
    @pass_call
    @pass_old_obj
    @pass_new_obj
    def validate_password(self, ctx, call, old_obj, new_obj, password):
        current_user = ctx['user']

        # Setting password
        if password is not None:
            # Can't change other user's passwords
            if old_obj.id is not None and new_obj != current_user or current_user.is_admin:
                raise ValidationError('Permission denied!')

            allow_weak_passwords = ctx.get('allow_weak_passwords', False)

            if not allow_weak_passwords and not is_strong_password(password, new_obj):
                raise ValidationError('Password is too weak.')

        return password

    @pass_context
    @pass_call
    @pass_old_obj
    @pass_new_obj
    @pass_old_value
    def validate_first_name(self, ctx, call, old_obj, new_obj, old_first_name, new_first_name):
        current_user = ctx['user']

        # First name has changed
        if old_obj.id is not None and new_first_name != old_first_name:
            # Regular user trying to change another user's first name
            if new_obj != current_user and not current_user.is_admin:
                raise ValidationError("Permission denied!")

        return new_first_name

    @pass_context
    @pass_call
    @pass_old_obj
    @pass_new_obj
    @pass_old_value
    def validate_last_name(self, ctx, call, old_obj, new_obj, old_last_name, new_last_name):
        current_user = ctx['user']

        # Last name has changed
        if old_obj.id is not None and old_last_name != new_last_name:
            # Regular user trying to change another user's last name
            if new_obj != current_user and not current_user.is_admin:
                raise ValidationError("Permission denied!")

        return new_last_name

    @pass_context
    @pass_call
    @pass_old_obj
    @pass_new_obj
    @pass_old_value
    def validate_email(self, ctx, call, old_obj, new_obj, old_email, new_email):
        current_user = ctx['user']

        # Email has changed
        if old_obj.id is not None and old_email != new_email:
            # Regular user trying to change another user's email
            if new_obj != current_user and not current_user.is_admin:
                raise ValidationError("Permission denied!")

        return new_email

    @pass_context
    @pass_old_obj
    @pass_new_obj
    def validate_force_password_change(self, ctx, old_obj, new_obj, value):
        current_user = ctx['user']

        if not current_user.is_admin:
            # New user
            if old_obj.id is None:
                if not new_obj.force_password_change:
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
                    # Can't unset flag without changing password
                    # NOTE we check the password has actually changed in the validate method
                    raise ValidationError('A password change is required.')

        return value

    @pass_context
    @pass_new_obj
    @pass_old_value
    def validate_is_admin(self, ctx, obj, old_is_admin, new_is_admin):
        current_user = ctx['user']

        if new_is_admin:
            # Must be an admin to grant admin rights
            if not old_is_admin and not current_user.is_admin:
                raise ValidationError('Permission denied!')
        else:
            # Can't revoke your own admin rights
            if old_is_admin and current_user == obj:
                raise ValidationError('Permission denied!')

        return new_is_admin

    @pass_context
    @pass_call
    @pass_old_obj
    def validate(self, ctx, call, old_obj, new_obj):
        current_user = ctx['user']

        # Password is required when creating a new user
        if old_obj.id is None:
            call.validators_for_field([required()], new_obj, self.password)

        # Humans need a name and email
        if not new_obj.is_bot:
            call.validators_for_field([not_empty()], new_obj, self.first_name)
            call.validators_for_field([not_empty()], new_obj, self.last_name)
            call.validators_for_field([required()], new_obj, self.email)

        # Check passwords if updating your own email or password
        if current_user == new_obj:
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
