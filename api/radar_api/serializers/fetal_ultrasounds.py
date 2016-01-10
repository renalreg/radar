from radar_api.serializers.sources import SourceGroupSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedStringSerializer
from radar.models.fetal_ultrasounds import FetalUltrasound, LIQUOR_VOLUMES


class FetalUltrasoundSerializer(PatientSerializerMixin, SourceGroupSerializerMixin, MetaSerializerMixin, ModelSerializer):
    liquor_volume = CodedStringSerializer(LIQUOR_VOLUMES)

    class Meta(object):
        model_class = FetalUltrasound
