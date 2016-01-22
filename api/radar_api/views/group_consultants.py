from radar_api.serializers.group_consultants import GroupConsultantSerializer
from radar.models.consultants import GroupConsultant
from radar.views.core import RetrieveUpdateDestroyModelView, ListCreateModelView
from radar.permissions import AdminPermission


class GroupConsultantListView(ListCreateModelView):
    serializer_class = GroupConsultantSerializer
    model_class = GroupConsultant
    permission_classes = [AdminPermission]


class GroupConsultantDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = GroupConsultantSerializer
    model_class = GroupConsultant
    permission_classes = [AdminPermission]


def register_views(app):
    app.add_url_rule('/group-consultants', view_func=GroupConsultantListView.as_view('group_consultant_list'))
    app.add_url_rule('/group-consultants/<int:id>', view_func=GroupConsultantDetailView.as_view('group_consultant_detail'))
