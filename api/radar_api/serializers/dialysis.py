from radar_api.serializers.sources import SourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.fields import LabelledIntegerField
from radar.models.dialysis import Dialysis, DIALYSIS_MODALITIES


class DialysisSerializer(MetaSerializerMixin, PatientSerializerMixin, SourceSerializerMixin, ModelSerializer):
    modality = LabelledIntegerField(DIALYSIS_MODALITIES)

    class Meta(object):
        model_class = Dialysis
