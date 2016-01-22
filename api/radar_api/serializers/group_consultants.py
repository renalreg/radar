from radar_api.serializers.consultant_fields import ConsultantReferenceField
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.groups import GroupReferenceField
from radar.models.consultants import GroupConsultant
from radar.serializers.models import ModelSerializer


class GroupConsultantSerializer(MetaSerializerMixin, ModelSerializer):
    group = GroupReferenceField()
    consultant = ConsultantReferenceField()

    class Meta(object):
        model_class = GroupConsultant
        exclude = ['group_id', 'consultant_id']
