from radar.api.serializers.data_sources import DataSourceSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.patient_mixins import PatientSerializerMixin
from radar.lib.serializers.models import ModelSerializer
from radar.lib.serializers.codes import CodedStringSerializer
from radar.lib.models import RenalImaging, RENAL_IMAGING_TYPES, RENAL_IMAGING_KIDNEY_TYPES


class RenalImagingSerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    imaging_type = CodedStringSerializer(RENAL_IMAGING_TYPES)
    right_type = CodedStringSerializer(RENAL_IMAGING_KIDNEY_TYPES)
    left_type = CodedStringSerializer(RENAL_IMAGING_KIDNEY_TYPES)

    class Meta(object):
        model_class = RenalImaging
