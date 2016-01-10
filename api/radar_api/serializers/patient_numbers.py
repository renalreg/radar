from radar_api.serializers.sources import SourceGroupSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.groups import GroupReferenceField
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.models import PatientNumber


class PatientNumberSerializer(PatientSerializerMixin, SourceGroupSerializerMixin, MetaSerializerMixin, ModelSerializer):
    group = GroupReferenceField()

    class Meta(object):
        model_class = PatientNumber
        exclude = ['group_id']
