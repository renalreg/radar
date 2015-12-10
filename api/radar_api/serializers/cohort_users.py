from radar_api.serializers.cohorts import CohortReferenceField
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.user_mixins import UserSerializerMixin
from radar.models import CohortUser
from radar.roles import COHORT_ROLE_NAMES
from radar.serializers.fields import ListField, StringField
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedStringSerializer


class CohortUserSerializer(UserSerializerMixin, MetaSerializerMixin, ModelSerializer):
    cohort = CohortReferenceField()
    role = CodedStringSerializer(COHORT_ROLE_NAMES)
    permissions = ListField(StringField(), read_only=True)

    class Meta(object):
        model_class = CohortUser
        exclude = ['user_id', 'cohort_id']
