from radar.api.permissions import AdminPermission
from radar.api.serializers.consultants import GroupConsultantSerializer
from radar.api.views.generics import (
    RetrieveUpdateDestroyModelView,
    ListCreateModelView
)
from radar.models.consultants import GroupConsultant


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
