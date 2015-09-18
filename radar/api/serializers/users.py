from radar.api.serializers.cohort_users import CohortUserSerializer
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.organisation_users import OrganisationUserSerializer
from radar.api.serializers.patients import OrganisationReferenceField, CohortReferenceField
from radar.lib.serializers import Serializer, IntegerField, StringField, ModelSerializer, ListField
from radar.lib.models import User


class UserSerializer(MetaSerializerMixin, ModelSerializer):
    organisations = ListField(field=OrganisationUserSerializer(), source='organisation_users', read_only=True)
    cohorts = ListField(field=CohortUserSerializer(), source='cohort_users', read_only=True)

    class Meta(object):
        model_class = User
        fields = ('id', 'is_admin', 'username', 'email', 'first_name', 'last_name')


class UserListRequestSerializer(Serializer):
    id = IntegerField()
    username = StringField()
    email = StringField()
    first_name = StringField()
    last_name = StringField()
    organisation_id = OrganisationReferenceField(write_only=True)
    cohort_id = CohortReferenceField(write_only=True)
