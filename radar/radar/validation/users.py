from radar.auth.passwords import check_password_hash, check_password_strength, WeakPasswordError
from radar.validation.core import Validation, Field, pass_old_obj, pass_context, ValidationError, pass_new_obj, \
    pass_call, pass_old_value
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import required, optional, email_address, not_empty, none_if_blank, default, max_length, lower
from radar.models.users import User


class PasswordField(Field):
    def set_value(self, obj, value):
        # Password is optional but we don't want to overwrite it with None
        if value is not None:
            super(PasswordField, self).set_value(obj, value)


class UserValidation(MetaValidationMixin, Validation):
    id = Field([optional()])
    username = Field([required()])  # TODO username()
    password = PasswordField([optional()])
    password_hash = Field([optional()])
    email = Field([none_if_blank(), optional(), lower(), email_address()])
    first_name = Field([none_if_blank(), optional()])
    last_name = Field([none_if_blank(), optional()])
    telephone_number = Field([none_if_blank(), optional(), max_length(100)])
    is_admin = Field([default(False), required()])
    force_password_change = Field([default(False), required()])

    @pass_context
    @pass_old_obj
    @pass_old_value
    def validate_username(self, ctx, old_obj, old_username, new_username):
        current_user = ctx['user']

        if old_obj.id is not None and old_username != new_username and not current_user.is_admin:
            raise ValidationError('Only admins can change usernames.')

        if old_obj.id is None or old_username != new_username:
            q = User.query.filter(User.username == new_username)

            # Ignore self
            if old_obj.id is not None:
                q = q.filter(User.id != old_obj.id)

            # Check username not already taken
            if q.count() > 0:
                raise ValidationError('Username already in use.')

        return new_username

    @pass_context
    @pass_call
    @pass_old_obj
    @pass_new_obj
    def validate_password(self, ctx, call, old_obj, new_obj, password):
        # Setting password
        if password is not None:
            allow_weak_passwords = ctx.get('allow_weak_passwords', False)

            if not allow_weak_passwords:
                try:
                    check_password_strength(password, new_obj)
                except WeakPasswordError as e:
                    raise ValidationError(e.message)

        return password

    @pass_context
    @pass_old_obj
    @pass_new_obj
    def validate_force_password_change(self, ctx, old_obj, new_obj, value):
        current_user = ctx['user']

        # New user
        if old_obj.id is None:
            if not new_obj.force_password_change and not current_user.is_admin:
                raise ValidationError('New users must be forced to change their password.')
        else:
            if (
                current_user == new_obj and
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
            # Note: if the user is editing themselves the current_user will have is_admin set
            if not old_is_admin and (current_user == obj or not current_user.is_admin):
                raise ValidationError('Must be an admin to grant admin rights.')
        else:
            # Can't revoke your own admin rights
            if old_is_admin and current_user == obj:
                raise ValidationError("Can't revoke your own admin rights.")

        return new_is_admin

    @pass_context
    @pass_new_obj
    @pass_old_value
    def validate_is_enabled(self, ctx, obj, old_is_enabled, new_is_enabled):
        current_user = ctx['user']

        if current_user == obj and old_is_enabled != new_is_enabled:
            raise ValidationError("Can't enable/disable your own account.")

        return new_is_enabled

    @pass_context
    @pass_call
    @pass_old_obj
    def validate(self, ctx, call, old_obj, new_obj):
        current_user = ctx['user']

        if old_obj.id is None:
            # Password is required when creating a new user
            call.validators_for_field([required()], new_obj, self.password)

            # New humans need a name and email
            # TODO users can blank their first name, last name and email
            if not new_obj.is_bot:
                call.validators_for_field([not_empty()], new_obj, self.first_name)
                call.validators_for_field([not_empty()], new_obj, self.last_name)
                call.validators_for_field([required()], new_obj, self.email)
        else:
            # Editing yourself
            if current_user == new_obj:
                # Current password is required to change email or password
                password_required = (
                    old_obj.email != new_obj.email or
                    old_obj.password_hash != new_obj.password_hash
                )

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
