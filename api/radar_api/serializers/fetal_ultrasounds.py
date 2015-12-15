from radar_api.serializers.data_sources import DataSourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedIntegerSerializer
from radar.models.fetal_ultrasounds import FetalUltrasound, LIQUOR_VOLUMES


class FetalUltrasoundSerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    liquor_volume = CodedIntegerSerializer(LIQUOR_VOLUMES)

    class Meta(object):
        model_class = FetalUltrasound
