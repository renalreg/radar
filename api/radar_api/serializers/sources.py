from radar_api.serializers.groups import GroupReferenceField


class SourceGroupSerializerMixin(object):
    source_group = GroupReferenceField()

    def get_model_exclude(self):
        attrs = super(SourceGroupSerializerMixin, self).get_model_exclude()
        attrs.add('source_group_id')
        return attrs
