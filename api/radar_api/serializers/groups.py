from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.fields import ListField, StringField
from radar.serializers.models import ModelSerializer, ReferenceField
from radar.models.groups import Group


class TinyGroupSerializer(ModelSerializer):
    class Meta(object):
        model_class = Group
        fields = ['id', 'type', 'code', 'name', 'short_name']


class GroupSerializer(MetaSerializerMixin, ModelSerializer):
    pages = ListField(StringField(), source='sorted_pages', read_only=True)

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
