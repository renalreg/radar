from radar_api.serializers.data_sources import DataSourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedStringSerializer
from radar.models.dialysis import Dialysis, TYPES_OF_DIALYSIS


class DialysisSerializer(MetaSerializerMixin, PatientSerializerMixin, DataSourceSerializerMixin, ModelSerializer):
    type_of_dialysis = CodedStringSerializer(TYPES_OF_DIALYSIS)

    class Meta(object):
        model_class = Dialysis
