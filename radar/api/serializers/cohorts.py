from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.serializers import ModelSerializer, ListField, ReferenceField
from radar.lib.models import CohortFeature, Cohort, CohortPatient


class CohortReferenceField(ReferenceField):
    model_class = Cohort


class CohortFeatureSerializer(ModelSerializer):
    class Meta:
        model_class = CohortFeature


class CohortSerializer(MetaSerializerMixin, ModelSerializer):
    features = ListField(field=CohortFeatureSerializer(), source='cohort_features')

    class Meta:
        model_class = Cohort


class CohortPatientSerializer(MetaSerializerMixin, ModelSerializer):
    cohort = CohortSerializer()

    class Meta:
        model_class = CohortPatient
        exclude = ['patient_id', 'cohort_id']


class BasicCohortSerializer(ModelSerializer):
    class Meta:
        model_class = Cohort


class CohortSerializerMixin(object):
    cohort = BasicCohortSerializer(read_only=True)
    cohort_id = CohortReferenceField()
