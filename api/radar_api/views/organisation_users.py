from radar_api.serializers.organisation_users import OrganisationUserSerializer
from radar.models import OrganisationUser
from radar.roles import ORGANISATION_ROLE_NAMES
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
    items = ORGANISATION_ROLE_NAMES


def register_views(app):
    app.add_url_rule('/organisation-users', view_func=OrganisationUserListView.as_view('organisation_user_list'))
    app.add_url_rule('/organisation-users/<int:id>', view_func=OrganisationUserDetailView.as_view('organisation_user_detail'))
    app.add_url_rule('/organisation-user-roles', view_func=OrganisationUserRoleListView.as_view('organisation_user_role_list'))
