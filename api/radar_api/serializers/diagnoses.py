from radar_api.serializers.groups import GroupSerializerMixin, TinyGroupSerializer
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.core import Serializer
from radar.serializers.fields import IntegerField
from radar.serializers.models import ModelSerializer, ReferenceField
from radar.models.diagnoses import Diagnosis, GroupDiagnosis, BiopsyDiagnosis, GroupBiopsyDiagnosis


class GroupDiagnosisSerializer(GroupSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = GroupDiagnosis


class GroupDiagnosisReferenceField(ReferenceField):
    model_class = GroupDiagnosis
    serializer_class = GroupDiagnosisSerializer


class BiopsyDiagnosisSerializer(ModelSerializer):
    class Meta(object):
        model_class = BiopsyDiagnosis


class GroupBiopsyDiagnosisSerializer(ModelSerializer):
    group = TinyGroupSerializer()
    biopsy_diagnosis = BiopsyDiagnosisSerializer()

    class Meta(object):
        model_class = GroupBiopsyDiagnosis
        exclude = ['group_id', 'biopsy_diagnosis_id']


class BiopsyDiagnosisReferenceField(ReferenceField):
    model_class = BiopsyDiagnosis
    serializer_class = BiopsyDiagnosisSerializer


class DiagnosisSerializer(PatientSerializerMixin, GroupSerializerMixin, MetaSerializerMixin, ModelSerializer):
    group_diagnosis = GroupDiagnosisReferenceField()
    age_of_symptoms = IntegerField(read_only=True)
    age_of_diagnosis = IntegerField(read_only=True)
    age_of_renal_disease = IntegerField(read_only=True)
    biopsy_diagnosis = BiopsyDiagnosisReferenceField()

    class Meta(object):
        model_class = Diagnosis
        exclude = ['group_diagnosis_id', 'biopsy_diagnosis_id']


class GroupDiagnosisRequestSerializer(Serializer):
    group = IntegerField()


class GroupBiopsyDiagnosisRequestSerializer(Serializer):
    group = IntegerField()
