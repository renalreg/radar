from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.organisations import OrganisationReferenceField
from radar_api.serializers.user_mixins import UserSerializerMixin
from radar.models import OrganisationUser
from radar.roles import ORGANISATION_ROLE_NAMES
from radar.serializers.fields import ListField, StringField
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedStringSerializer


class OrganisationUserSerializer(UserSerializerMixin, MetaSerializerMixin, ModelSerializer):
    organisation = OrganisationReferenceField()
    role = CodedStringSerializer(ORGANISATION_ROLE_NAMES)
    permissions = ListField(StringField(), read_only=True)

    class Meta(object):
        model_class = OrganisationUser
        exclude = ['user_id', 'organisation_id']
