from radar_api.serializers.sources import SourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.fields import LabelledStringField
from radar.models.renal_imaging import RenalImaging, RENAL_IMAGING_TYPES, RENAL_IMAGING_KIDNEY_TYPES


class RenalImagingSerializer(PatientSerializerMixin, SourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    imaging_type = LabelledStringField(RENAL_IMAGING_TYPES)
    right_type = LabelledStringField(RENAL_IMAGING_KIDNEY_TYPES)
    left_type = LabelledStringField(RENAL_IMAGING_KIDNEY_TYPES)

    class Meta(object):
        model_class = RenalImaging
