from radar_api.serializers.sources import SourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.fields import LabelledStringField
from radar.models.nephrectomies import Nephrectomy, NEPHRECTOMY_KIDNEY_SIDES, \
    NEPHRECTOMY_KIDNEY_TYPES, NEPHRECTOMY_ENTRY_TYPES


class NephrectomySerializer(PatientSerializerMixin, SourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    kidney_side = LabelledStringField(NEPHRECTOMY_KIDNEY_SIDES)
    kidney_type = LabelledStringField(NEPHRECTOMY_KIDNEY_TYPES)
    entry_type = LabelledStringField(NEPHRECTOMY_ENTRY_TYPES)

    class Meta(object):
        model_class = Nephrectomy
