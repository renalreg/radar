from radar.api.serializers.data_sources import DataSourceSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.patient_mixins import PatientSerializerMixin
from radar.lib.serializers import ModelSerializer, CodedStringSerializer
from radar.lib.models import PATHOLOGY_KIDNEY_TYPES, PATHOLOGY_KIDNEY_SIDES, Pathology


class PathologySerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    kidney_type = CodedStringSerializer(PATHOLOGY_KIDNEY_TYPES)
    kidney_side = CodedStringSerializer(PATHOLOGY_KIDNEY_SIDES)

    class Meta(object):
        model_class = Pathology
