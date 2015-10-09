from radar_api.serializers.organisation_users import OrganisationUserSerializer
from radar.models import OrganisationUser
from radar.roles import ORGANISATION_ROLES
from radar.validation.organisation_users import OrganisationUserValidation
from radar.views.codes import CodedStringListView
from radar.views.core import RetrieveUpdateDestroyModelView, ListCreateModelView


class OrganisationUserListView(ListCreateModelView):
    serializer_class = OrganisationUserSerializer
    model_class = OrganisationUser
    validation_class = OrganisationUserValidation


class OrganisationUserDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = OrganisationUserSerializer
    model_class = OrganisationUser
    validation_class = OrganisationUserValidation


class OrganisationUserRoleListView(CodedStringListView):
    items = ORGANISATION_ROLES
