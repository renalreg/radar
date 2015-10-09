from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.organisations import OrganisationReferenceField
from radar_api.serializers.user_mixins import UserSerializerMixin
from radar.models import OrganisationUser
from radar.roles import ORGANISATION_ROLES
from radar.serializers.fields import BooleanField
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedStringSerializer


class OrganisationUserSerializer(UserSerializerMixin, MetaSerializerMixin, ModelSerializer):
    has_view_demographics_permission = BooleanField(read_only=True)
    has_view_patient_permission = BooleanField(read_only=True)
    has_edit_patient_permission = BooleanField(read_only=True)
    has_recruit_patient_permission = BooleanField(read_only=True)
    has_view_user_permission = BooleanField(read_only=True)
    has_edit_user_membership_permission = BooleanField(read_only=True)
    organisation = OrganisationReferenceField()
    role = CodedStringSerializer(ORGANISATION_ROLES)

    class Meta(object):
        model_class = OrganisationUser
        exclude = ['user_id', 'organisation_id']
