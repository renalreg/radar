from radar_api.serializers.groups import GroupSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.core import Serializer
from radar.serializers.fields import IntegerField
from radar.serializers.models import ModelSerializer, ReferenceField
from radar.serializers.fields import LabelledIntegerField
from radar.models.diagnoses import Diagnosis, DIAGNOSIS_BIOPSY_DIAGNOSES, GroupDiagnosis


class GroupDiagnosisSerializer(GroupSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = GroupDiagnosis


class GroupDiagnosisReferenceField(ReferenceField):
    model_class = GroupDiagnosis
    serializer_class = GroupDiagnosisSerializer


class DiagnosisSerializer(PatientSerializerMixin, GroupSerializerMixin, MetaSerializerMixin, ModelSerializer):
    group_diagnosis = GroupDiagnosisReferenceField()
    biopsy_diagnosis = LabelledIntegerField(DIAGNOSIS_BIOPSY_DIAGNOSES)
    age_of_symptoms = IntegerField(read_only=True)
    age_of_diagnosis = IntegerField(read_only=True)
    age_of_renal_disease = IntegerField(read_only=True)

    class Meta(object):
        model_class = Diagnosis
        exclude = ['group_diagnosis_id']


class GroupDiagnosisRequestSerializer(Serializer):
    group = IntegerField()
