from radar.api.serializers.cohorts import CohortReferenceField
from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.models import CohortUser
from radar.lib.roles import COHORT_ROLES
from radar.lib.serializers import ModelSerializer, BooleanField, CodedStringSerializer


class CohortUserSerializer(MetaSerializerMixin, ModelSerializer):
    has_view_demographics_permission = BooleanField()
    has_view_patient_permission = BooleanField()
    has_edit_patient_permission = BooleanField()
    has_view_user_permission = BooleanField()
    has_edit_user_membership_permission = BooleanField()
    cohort = CohortReferenceField()
    role = CodedStringSerializer(COHORT_ROLES)

    class Meta(object):
        model_class = CohortUser
        exclude = ['user_id']
