from radar_api.serializers.data_sources import DataSourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedStringSerializer
from radar.models import PATHOLOGY_KIDNEY_TYPES, PATHOLOGY_KIDNEY_SIDES, Pathology


class PathologySerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    kidney_type = CodedStringSerializer(PATHOLOGY_KIDNEY_TYPES)
    kidney_side = CodedStringSerializer(PATHOLOGY_KIDNEY_SIDES)

    class Meta(object):
        model_class = Pathology
