from radar_api.serializers.sources import SourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.groups import GroupReferenceField
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.models.patient_numbers import PatientNumber


class PatientNumberSerializer(PatientSerializerMixin, SourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    number_group = GroupReferenceField()

    class Meta(object):
        model_class = PatientNumber
        exclude = ['group_id']
