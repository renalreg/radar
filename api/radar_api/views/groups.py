from radar_api.serializers.groups import GroupSerializer
from radar.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView
from radar.models.groups import Group
from radar.permissions import AdminWritePermission
from radar.validation.groups import GroupValidation


class GroupListView(ListCreateModelView):
    serializer_class = GroupSerializer
    model_class = Group
    validation_class = GroupValidation
    permission_classes = [AdminWritePermission]


class GroupDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = GroupSerializer
    model_class = Group
    validation_class = GroupValidation
    permission_classes = [AdminWritePermission]


def register_views(app):
    app.add_url_rule('/groups', view_func=GroupListView.as_view('group_list'))
    app.add_url_rule('/groups/<int:id>', view_func=GroupDetailView.as_view('group_detail'))
