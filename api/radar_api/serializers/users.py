from radar_api.serializers.cohort_users import CohortUserSerializer
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.organisation_users import OrganisationUserSerializer
from radar_api.serializers.patients import OrganisationReferenceField, CohortReferenceField
from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, IntegerField, ListField, BooleanField
from radar.serializers.models import ModelSerializer
from radar.models import User


class UserSerializer(MetaSerializerMixin, ModelSerializer):
    id = IntegerField()
    is_admin = BooleanField()
    username = StringField()
    email = StringField()
    first_name = StringField()
    last_name = StringField()
    force_password_change = BooleanField()
    telephone_number = StringField()

    organisations = ListField(field=OrganisationUserSerializer(), source='organisation_users', read_only=True)
    cohorts = ListField(field=CohortUserSerializer(), source='cohort_users', read_only=True)

    current_password = StringField(write_only=True)
    password = StringField(write_only=True)

    class Meta:
        model_class = User
        fields = (
            'id',
            'is_admin',
            'username',
            'email',
            'first_name',
            'last_name',
            'telephoneNumber',
            'force_password_change',
        )


class UserListRequestSerializer(Serializer):
    id = IntegerField()
    username = StringField()
    email = StringField()
    first_name = StringField()
    last_name = StringField()
    organisation = OrganisationReferenceField(write_only=True)
    cohort = CohortReferenceField(write_only=True)
