from radar.api.serializers.cohorts import CohortReferenceField
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.user_mixins import UserSerializerMixin
from radar.lib.models import CohortUser
from radar.lib.roles import COHORT_ROLES
from radar.lib.serializers.fields import BooleanField
from radar.lib.serializers.models import ModelSerializer
from radar.lib.serializers.codes import CodedStringSerializer


class CohortUserSerializer(UserSerializerMixin, MetaSerializerMixin, ModelSerializer):
    has_view_demographics_permission = BooleanField(read_only=True)
    has_view_patient_permission = BooleanField(read_only=True)
    has_edit_patient_permission = BooleanField(read_only=True)
    has_view_user_permission = BooleanField(read_only=True)
    has_edit_user_membership_permission = BooleanField(read_only=True)
    cohort = CohortReferenceField()
    role = CodedStringSerializer(COHORT_ROLES)

    class Meta(object):
        model_class = CohortUser
        exclude = ['user_id', 'cohort_id']
