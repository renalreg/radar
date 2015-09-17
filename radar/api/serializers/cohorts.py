from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.serializers import ModelSerializer, ListField, ReferenceField
from radar.lib.models import CohortFeature, Cohort, CohortPatient


class BasicCohortSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = Cohort


class CohortReferenceField(ReferenceField):
    model_class = Cohort
    serializer_class = BasicCohortSerializer


class CohortFeatureSerializer(ModelSerializer):
    class Meta(object):
        model_class = CohortFeature


class CohortSerializer(MetaSerializerMixin, ModelSerializer):
    features = ListField(field=CohortFeatureSerializer(), source='cohort_features')

    class Meta(object):
        model_class = Cohort


class CohortPatientSerializer(MetaSerializerMixin, ModelSerializer):
    cohort = CohortSerializer()

    class Meta(object):
        model_class = CohortPatient
        exclude = ['patient_id', 'cohort_id']


class CohortSerializerMixin(object):
    cohort = CohortReferenceField()

    def get_model_exclude(self):
        attrs = super(CohortSerializerMixin, self).get_model_exclude()
        attrs.add('cohort_id')
        return attrs
