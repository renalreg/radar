from radar_api.serializers.group_users import GroupUserSerializer
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.groups import GroupReferenceField
from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, IntegerField, ListField, BooleanField, CommaSeparatedField
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
