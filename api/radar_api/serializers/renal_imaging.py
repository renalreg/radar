from radar_api.serializers.data_sources import DataSourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedStringSerializer
from radar.models import RenalImaging, RENAL_IMAGING_TYPES, RENAL_IMAGING_KIDNEY_TYPES


class RenalImagingSerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    imaging_type = CodedStringSerializer(RENAL_IMAGING_TYPES)
    right_type = CodedStringSerializer(RENAL_IMAGING_KIDNEY_TYPES)
    left_type = CodedStringSerializer(RENAL_IMAGING_KIDNEY_TYPES)

    class Meta(object):
        model_class = RenalImaging
