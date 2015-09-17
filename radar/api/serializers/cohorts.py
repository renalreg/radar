from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.roles import COHORT_ROLES
from radar.lib.serializers import ModelSerializer, ListField, ReferenceField, BooleanField, CodedStringSerializer
from radar.lib.models import CohortFeature, Cohort, CohortPatient, CohortUser


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


class CohortUserSerializer(MetaSerializerMixin, ModelSerializer):
    has_view_demographics_permission = BooleanField()
    has_view_patient_permission = BooleanField()
    has_edit_patient_permission = BooleanField()
    has_view_user_permission = BooleanField()
    has_edit_user_membership_permission = BooleanField()
    cohort = CohortSerializer()
    role = CodedStringSerializer(COHORT_ROLES)

    class Meta(object):
        model_class = CohortUser
        exclude = ['user_id', 'cohort_id']


class CohortSerializerMixin(object):
    cohort = CohortReferenceField()

    def get_model_exclude(self):
        attrs = super(CohortSerializerMixin, self).get_model_exclude()
        attrs.add('cohort_id')
        return attrs
