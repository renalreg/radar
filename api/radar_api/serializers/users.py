from radar_api.serializers.group_users import GroupUserSerializer
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.groups import GroupReferenceField
from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, IntegerField, ListField, BooleanField, CommaSeparatedField, DateTimeField
from radar.serializers.models import ModelSerializer
from radar.models.users import User


class UserSerializer(MetaSerializerMixin, ModelSerializer):
    id = IntegerField()
    is_admin = BooleanField()
    username = StringField()
    email = StringField()
    first_name = StringField()
    last_name = StringField()
    force_password_change = BooleanField()
    telephone_number = StringField()
    is_enabled = BooleanField()

    last_login_date = DateTimeField(read_only=True)
    last_active_date = DateTimeField(read_only=True)

    groups = ListField(field=GroupUserSerializer(), source='group_users', read_only=True)

    current_password = StringField(write_only=True)
    password = StringField(write_only=True)

    class Meta:
        model_class = User
        fields = (
            'id',
            'is_admin',
            'username',
            'email',
            'first_name',
            'last_name',
            'telephoneNumber',
            'force_password_change',
        )


class UserListRequestSerializer(Serializer):
    id = IntegerField()
    username = StringField()
    email = StringField()
    first_name = StringField()
    last_name = StringField()
    group = CommaSeparatedField(GroupReferenceField())
    is_enabled = BooleanField()
    is_admin = BooleanField()
    has_logged_in = BooleanField()
