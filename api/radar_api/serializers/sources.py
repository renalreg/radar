from radar_api.serializers.groups import GroupReferenceField
from radar_api.serializers.source_types import SourceTypeReferenceField


class SourceGroupSerializerMixin(object):
    source_group = GroupReferenceField()
    source_type = SourceTypeReferenceField()

    def get_model_exclude(self):
        attrs = super(SourceGroupSerializerMixin, self).get_model_exclude()
        attrs.add('source_group_id')
        return attrs
