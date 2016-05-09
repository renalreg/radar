from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.validators import (
    none_if_blank,
    optional,
    lower,
    email_address,
    max_length,
    not_empty,
    required
)
from cornflake.exceptions import ValidationError

from radar.auth.passwords import check_password_strength, WeakPasswordError
from radar.auth.sessions import logout_other_sessions, logout_user
from radar.api.serializers.common import MetaMixin
from radar.api.serializers.group_users import GroupUserSerializer
from radar.models.users import User


class UserSerializer(MetaMixin, ModelSerializer):
    id = fields.IntegerField(read_only=True)
    username = fields.StringField()  # TODO username()
    email = fields.StringField(required=False, validators=[none_if_blank(), optional(), lower(), email_address()])
    first_name = fields.StringField(required=False, validators=[none_if_blank(), optional()])
    last_name = fields.StringField(required=False, validators=[none_if_blank(), optional()])
    telephone_number = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(100)])
    force_password_change = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)
    is_enabled = fields.BooleanField(default=True)
    is_bot = fields.BooleanField(default=False)

    last_login_date = fields.DateTimeField(read_only=True)
    last_active_date = fields.DateTimeField(read_only=True)

    groups = fields.ListField(child=GroupUserSerializer(), source='group_users', read_only=True)

    current_password = fields.StringField(required=False, write_only=True)
    password = fields.StringField(required=False, write_only=True)

    class Meta(object):
        model_class = User
        fields = []

    def validate_username(self, username):
        current_user = self.context['user']
        instance = self.instance

        if instance is not None and instance.username != username and not current_user.is_admin:
            raise ValidationError('Must be an admin to change usernames.')

        # Check for duplicate usernames
        if instance is None or instance.username != username:
            q = User.query.filter(User.username == username)

            # Ignore self
            if instance is not None:
                q = q.filter(User.id != instance.id)

            # Check username not already taken
            if q.count() > 0:
                raise ValidationError('Username already in use.')

        return username

    def validate_email(self, email):
        current_user = self.context['user']
        instance = self.instance

        if instance is not None and instance.is_admin and not current_user.is_admin:
            raise ValidationError("Must be an admin to change other admin's email addresses.")

        return email

    def validate_force_password_change(self, force_password_change):
        current_user = self.context['user']
        instance = self.instance

        if instance is None and not force_password_change and not current_user.is_admin:
            raise ValidationError('New users must be forced to change their password.')

        return force_password_change

    def validate_is_admin(self, is_admin):
        current_user = self.context['user']
        instance = self.instance

        if is_admin:
            # Must be an admin to grant admin rights
            if (instance is None or not instance.is_admin) and not current_user.is_admin:
                raise ValidationError('Must be an admin to grant admin rights.')
        else:
            # Can't revoke your own admin rights
            if instance is not None and instance.is_admin and instance == current_user:
                raise ValidationError("Can't revoke your own admin rights.")

            # Can't revoke other user's admin rights unless you are an admin
            if instance is not None and instance.is_admin and not current_user.is_admin:
                raise ValidationError('Must be an admin to revoke admin rights.')

        return is_admin

    def validate_is_enabled(self, is_enabled):
        current_user = self.context['user']
        instance = self.instance

        if instance is None:
            if not is_enabled:
                raise ValidationError("Can't create a disabled account.")
        else:
            if instance.is_enabled != is_enabled:
                if instance == current_user:
                    raise ValidationError("Can't enable/disable your own account.")

                if instance.is_admin and not current_user.is_admin:
                    raise ValidationError("Must be an admin to enable/disable an admin account.")

        return is_enabled

    def validate_is_bot(self, is_bot):
        current_user = self.context['user']
        instance = self.instance

        if instance is None:
            if is_bot and not current_user.is_admin:
                raise ValidationError('Must be an admin to create bots.')
        else:
            if instance.is_bot != is_bot:
                if instance == current_user:
                    raise ValidationError("Can't modify your own bot flag.")

                if not current_user.is_admin:
                    raise ValidationError('Must be an admin to modify the bot flag.')

        return is_bot

    def validate_password(self, password):
        allow_weak_passwords = self.context.get('allow_weak_passwords', False)

        if not allow_weak_passwords:
            try:
                # TODO pass user argument to check_password_strength
                check_password_strength(password)
            except WeakPasswordError as e:
                raise ValidationError(e.message)

        return password

    def validate(self, data):
        data = super(UserSerializer, self).validate(data)

        current_user = self.context['user']
        instance = self.instance

        if not data['is_bot']:
            # Humans need a name and email
            self.run_validators_on_field(data, self.first_name, [not_empty()])
            self.run_validators_on_field(data, self.last_name, [not_empty()])
            self.run_validators_on_field(data, self.email, [required()])

        # New user
        if instance is None:
            # Password is required when creating a new user
            if not data['is_bot']:
                self.run_validators_on_field(data, self.password, [required()])
        else:
            # Editing yourself
            if current_user == instance:
                password = data['password']
                current_password = data['current_password']

                # Current password is required to change email or password
                if (
                    (
                        instance.email != data['email'] or
                        (password is not None and not instance.check_password(password))
                    ) and
                    (
                        current_password is None or
                        not instance.check_password(current_password)
                    )
                ):
                    # Incorrect password
                    raise ValidationError({'current_password': 'Incorrect password!'})

                # Trying to disable force password change flag
                if instance.force_password_change and not data['force_password_change']:
                    if password is None:
                        raise ValidationError({'password': 'Must supply a new password.'})
                    elif instance.check_password(password):
                        # New password must be different to old password if force password change was set
                        raise ValidationError({'password': 'New password must be different to old password.'})

        return data

    def _save(self, instance, data):
        instance.is_admin = data['is_admin']
        instance.username = data['is_admin']
        instance.email = data['is_admin']
        instance.first_name = data['is_admin']
        instance.last_name = data['is_admin']
        instance.force_password_change = data['is_admin']
        instance.telephone_number = data['is_admin']
        instance.is_enabled = data['is_admin']

        # Password is only required for certain changes
        if data['password'] is not None:
            instance.password = data['password']

    def create(self, data):
        instance = User()
        self._save(instance, data)
        return instance

    def update(self, instance, data):
        # Changed password or email
        if data['password'] is not None or instance.email != data['email']:
            current_user = self.context['user']

            # Changed own password or email
            if current_user == instance:
                logout_other_sessions()
            else:
                logout_user(instance)

        self._save(instance, data)

        return instance
