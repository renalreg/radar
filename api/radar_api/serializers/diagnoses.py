from radar_api.serializers.groups import TinyGroupSerializer
from radar_api.serializers.sources import SourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.core import Serializer
from radar.serializers.fields import IntegerField, EnumField, LabelledIntegerField, ListField, CommaSeparatedField
from radar.serializers.models import ModelSerializer, ReferenceField
from radar.models.diagnoses import Diagnosis, GROUP_DIAGNOSIS_TYPE, BIOPSY_DIAGNOSES, PatientDiagnosis


class GroupDiagnosisSerializer(Serializer):
    group = TinyGroupSerializer()
    type = EnumField(GROUP_DIAGNOSIS_TYPE)


class DiagnosisSerializer(ModelSerializer):
    groups = ListField(GroupDiagnosisSerializer(), source='group_diagnoses')

    class Meta(object):
        model_class = Diagnosis


class TinyDiagnosisSerializer(ModelSerializer):
    class Meta(object):
        model_class = Diagnosis


class DiagnosisReferenceField(ReferenceField):
    model_class = Diagnosis
    serializer_class = TinyDiagnosisSerializer


class PatientDiagnosisSerializer(PatientSerializerMixin, SourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    diagnosis = DiagnosisReferenceField()
    symptoms_age = IntegerField(read_only=True)
    from_age = IntegerField(read_only=True)
    to_age = IntegerField(read_only=True)
    biopsy_diagnosis = LabelledIntegerField(BIOPSY_DIAGNOSES)

    class Meta(object):
        model_class = PatientDiagnosis
        exclude = ['diagnosis_id']


class DiagnosisRequestSerializer(Serializer):
    primary_group = CommaSeparatedField(IntegerField())
    secondary_group = CommaSeparatedField(IntegerField())
