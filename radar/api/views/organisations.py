from radar.api.serializers.organisations import OrganisationSerializer
from radar.lib.roles import ORGANISATION_ROLES
from radar.lib.views.core import ListModelView, CodedStringListView
from radar.lib.models import Organisation


class OrganisationListView(ListModelView):
    serializer_class = OrganisationSerializer
    model_class = Organisation


class OrganisationRoleListView(CodedStringListView):
    items = ORGANISATION_ROLES
