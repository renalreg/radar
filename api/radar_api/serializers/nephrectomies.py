from radar_api.serializers.data_sources import DataSourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedStringSerializer
from radar.models.nephrectomies import Nephrectomy, NEPHRECTOMY_KIDNEY_SIDES, \
    NEPHRECTOMY_KIDNEY_TYPES, NEPHRECTOMY_ENTRY_TYPES


class NephrectomySerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    kidney_side = CodedStringSerializer(NEPHRECTOMY_KIDNEY_SIDES)
    kidney_type = CodedStringSerializer(NEPHRECTOMY_KIDNEY_TYPES)
    entry_type = CodedStringSerializer(NEPHRECTOMY_ENTRY_TYPES)

    class Meta(object):
        model_class = Nephrectomy
