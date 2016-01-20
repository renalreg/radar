from radar_api.serializers.sources import SourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.fields import LabelledStringField
from radar.models.pathology import PATHOLOGY_KIDNEY_TYPES, PATHOLOGY_KIDNEY_SIDES, Pathology


class PathologySerializer(PatientSerializerMixin, SourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    kidney_type = LabelledStringField(PATHOLOGY_KIDNEY_TYPES)
    kidney_side = LabelledStringField(PATHOLOGY_KIDNEY_SIDES)

    class Meta(object):
        model_class = Pathology
