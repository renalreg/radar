from cornflake import fields
from cornflake import serializers
from cornflake.exceptions import ValidationError

from radar.auth.passwords import check_password_strength, WeakPasswordError


class LoginSerializer(serializers.Serializer):
    username = fields.StringField()
    password = fields.StringField()
    logout_other_sessions = fields.BooleanField(required=False)


class TokenSerializer(serializers.Serializer):
    user_id = fields.IntegerField()
    token = fields.StringField()


class ForgotPasswordSerializer(serializers.Serializer):
    username = fields.StringField()
    email = fields.StringField()


class ForgotUsernameSerializer(serializers.Serializer):
    email = fields.StringField()


class ResetPasswordSerializer(serializers.Serializer):
    token = fields.StringField()
    username = fields.StringField()
    password = fields.StringField()

    def validate_password(self, password):
        try:
            # TODO pass user argument to check_password_strength (this prevents the
            # user setting their password to their username etc.).
            check_password_strength(password)
        except WeakPasswordError as e:
            raise ValidationError(e.message)

        return password


class PasswordSerializer(serializers.Serializer):
    password = fields.StringField()
