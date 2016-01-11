from radar_api.serializers.groups import GroupReferenceField
from radar.serializers.models import ModelSerializer
from radar.models.source_types import SourceType


class SourceGroupSerializerMixin(object):
    source_group = GroupReferenceField()

    def get_model_exclude(self):
        attrs = super(SourceGroupSerializerMixin, self).get_model_exclude()
        attrs.add('source_group_id')
        return attrs


class SourceTypeSerializer(ModelSerializer):
    class Meta(object):
        model_class = SourceType
