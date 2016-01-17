from radar_api.serializers.groups import TinyGroupReferenceField
from radar.serializers.fields import StringField


class SourceSerializerMixin(object):
    source_group = TinyGroupReferenceField()
    source_type = StringField()

    def get_model_exclude(self):
        attrs = super(SourceSerializerMixin, self).get_model_exclude()
        attrs.add('source_group_id')
        return attrs
