from radar_api.serializers.groups import GroupReferenceField
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.user_mixins import UserSerializerMixin
from radar.models.groups import GroupUser
from radar.roles import ROLE, ROLE_NAMES
from radar.serializers.fields import ListField, StringField
from radar.serializers.models import ModelSerializer
from radar.serializers.fields import LabelledEnumField


class GroupUserSerializer(UserSerializerMixin, MetaSerializerMixin, ModelSerializer):
    group = GroupReferenceField()
    role = LabelledEnumField(ROLE, ROLE_NAMES)
    permissions = ListField(StringField(), read_only=True)

    class Meta(object):
        model_class = GroupUser
        exclude = ['user_id', 'group_id']
