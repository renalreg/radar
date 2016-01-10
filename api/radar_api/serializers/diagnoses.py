from radar_api.serializers.groups import CohortSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.core import Serializer
from radar.serializers.fields import IntegerField
from radar.serializers.models import ModelSerializer, ReferenceField
from radar.serializers.codes import CodedIntegerSerializer
from radar.models import Diagnosis, DIAGNOSIS_BIOPSY_DIAGNOSES, CohortDiagnosis


class CohortDiagnosisSerializer(CohortSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = CohortDiagnosis


class CohortDiagnosisReferenceField(ReferenceField):
    model_class = CohortDiagnosis
    serializer_class = CohortDiagnosisSerializer


class DiagnosisSerializer(PatientSerializerMixin, CohortSerializerMixin, MetaSerializerMixin, ModelSerializer):
    cohort_diagnosis = CohortDiagnosisReferenceField()
    biopsy_diagnosis = CodedIntegerSerializer(DIAGNOSIS_BIOPSY_DIAGNOSES)
    age_of_symptoms = IntegerField(read_only=True)
    age_of_diagnosis = IntegerField(read_only=True)
    age_of_renal_disease = IntegerField(read_only=True)

    class Meta(object):
        model_class = Diagnosis
        exclude = ['cohort_diagnosis_id']


class CohortDiagnosisRequestSerializer(Serializer):
    cohort = IntegerField()
