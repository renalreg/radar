from radar_api.serializers.groups import TinyGroupReferenceField
from radar_api.serializers.source_types import SourceTypeReferenceField


class SourceSerializerMixin(object):
    source_group = TinyGroupReferenceField()
    source_type = SourceTypeReferenceField()

    def get_model_exclude(self):
        attrs = super(SourceSerializerMixin, self).get_model_exclude()
        attrs.add('source_group_id')
        attrs.add('source_type_id')
        return attrs
