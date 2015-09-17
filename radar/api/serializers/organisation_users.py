from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.organisations import OrganisationReferenceField
from radar.lib.models import OrganisationUser
from radar.lib.roles import ORGANISATION_ROLES
from radar.lib.serializers import ModelSerializer, BooleanField, CodedStringSerializer


class OrganisationUserSerializer(MetaSerializerMixin, ModelSerializer):
    has_view_demographics_permission = BooleanField()
    has_view_patient_permission = BooleanField()
    has_edit_patient_permission = BooleanField()
    has_view_user_permission = BooleanField()
    has_edit_user_membership_permission = BooleanField()
    has_recruit_patient_permission = BooleanField()
    organisation = OrganisationReferenceField()
    role = CodedStringSerializer(ORGANISATION_ROLES)

    class Meta(object):
        model_class = OrganisationUser
        exclude = ['user_id', 'organisation_id']
