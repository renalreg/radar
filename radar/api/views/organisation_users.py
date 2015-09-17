from radar.api.serializers.organisations import OrganisationUserSerializer
from radar.lib.models import OrganisationUser
from radar.lib.roles import ORGANISATION_ROLES
from radar.lib.validation.organisation_users import OrganisationUserValidation
from radar.lib.views.codes import CodedStringListView
from radar.lib.views.core import RetrieveUpdateDestroyModelView, ListCreateModelView


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
