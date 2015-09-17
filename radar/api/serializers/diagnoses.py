from radar.api.serializers.cohorts import CohortSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.patient_mixins import PatientSerializerMixin
from radar.lib.serializers import ModelSerializer, CodedStringSerializer, ReferenceField, CodedIntegerSerializer
from radar.lib.models import Diagnosis, DIAGNOSIS_BIOPSY_DIAGNOSES, DIAGNOSIS_KARYOTYPES, CohortDiagnosis


class CohortDiagnosisSerializer(CohortSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = CohortDiagnosis


class CohortDiagnosisReferenceField(ReferenceField):
    model_class = CohortDiagnosis
    serializer_class = CohortDiagnosisSerializer


class DiagnosisSerializer(PatientSerializerMixin, CohortSerializerMixin, MetaSerializerMixin, ModelSerializer):
    cohort_diagnosis = CohortDiagnosisReferenceField()
    biopsy_diagnosis = CodedIntegerSerializer(DIAGNOSIS_BIOPSY_DIAGNOSES)
    karyotype = CodedIntegerSerializer(DIAGNOSIS_KARYOTYPES)

    class Meta(object):
        model_class = Diagnosis
        exclude = ['cohort_diagnosis_id']
