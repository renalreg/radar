from radar_api.serializers.organisation_consultants import OrganisationConsultantSerializer
from radar.models import OrganisationConsultant
from radar.views.core import RetrieveUpdateDestroyModelView, ListCreateModelView
from radar.permissions import AdminPermission


class OrganisationConsultantListView(ListCreateModelView):
    serializer_class = OrganisationConsultantSerializer
    model_class = OrganisationConsultant
    permission_classes = [AdminPermission]


class OrganisationConsultantDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = OrganisationConsultantSerializer
    model_class = OrganisationConsultant
    permission_classes = [AdminPermission]


def register_views(app):
    app.add_url_rule('/organisation-consultants', view_func=OrganisationConsultantListView.as_view('organisation_consultant_list'))
    app.add_url_rule('/organisation-consultants/<int:id>', view_func=OrganisationConsultantDetailView.as_view('organisation_consultant_detail'))
