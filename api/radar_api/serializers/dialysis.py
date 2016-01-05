from radar_api.serializers.data_sources import DataSourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedIntegerSerializer
from radar.models.dialysis import Dialysis, DIALYSIS_MODALITIES


class DialysisSerializer(MetaSerializerMixin, PatientSerializerMixin, DataSourceSerializerMixin, ModelSerializer):
    modality = CodedIntegerSerializer(DIALYSIS_MODALITIES)

    class Meta(object):
        model_class = Dialysis
