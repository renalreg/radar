from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.models.renal_diagnoses import RenalDiagnosis


class RenalDiagnosisSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = RenalDiagnosis
