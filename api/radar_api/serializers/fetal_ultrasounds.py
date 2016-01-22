from radar_api.serializers.sources import SourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.fields import LabelledStringField
from radar.models.fetal_ultrasounds import FetalUltrasound, LIQUOR_VOLUMES


class FetalUltrasoundSerializer(PatientSerializerMixin, SourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    liquor_volume = LabelledStringField(LIQUOR_VOLUMES)

    class Meta(object):
        model_class = FetalUltrasound
