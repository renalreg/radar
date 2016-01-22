from radar.serializers.core import Serializer
from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.fields import ListField, StringField, BooleanField, EnumField
from radar.serializers.models import ModelSerializer, ReferenceField
from radar.models.groups import Group, GROUP_TYPE


class TinyGroupSerializer(ModelSerializer):
    type = EnumField(GROUP_TYPE)

    class Meta(object):
        model_class = Group
        fields = ['id', 'type', 'code', 'name', 'short_name']


class GroupSerializer(MetaSerializerMixin, ModelSerializer):
    type = EnumField(GROUP_TYPE)
    pages = ListField(StringField(), read_only=True)

    class Meta(object):
        model_class = Group


class GroupReferenceField(ReferenceField):
    model_class = Group
    serializer_class = GroupSerializer


class TinyGroupReferenceField(ReferenceField):
    model_class = Group
    serializer_class = TinyGroupSerializer


class GroupSerializerMixin(object):
    group = GroupReferenceField()

    def get_model_exclude(self):
        attrs = super(GroupSerializerMixin, self).get_model_exclude()
        attrs.add('group_id')
        return attrs


class GroupListRequestSerializer(Serializer):
    code = StringField()
    type = EnumField(GROUP_TYPE)
    recruitment = BooleanField()
