from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.organisations import OrganisationReferenceField
from radar_api.serializers.user_mixins import UserSerializerMixin
from radar.models import OrganisationUser
from radar.roles import ORGANISATION_ROLES
from radar.serializers.fields import ListField, StringField, EnumField
from radar.serializers.models import ModelSerializer


class OrganisationUserSerializer(UserSerializerMixin, MetaSerializerMixin, ModelSerializer):
    organisation = OrganisationReferenceField()
    role = EnumField(ORGANISATION_ROLES)
    permissions = ListField(StringField(), read_only=True)

    class Meta(object):
        model_class = OrganisationUser
        exclude = ['user_id', 'organisation_id']
