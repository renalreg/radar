from radar_api.serializers.group_users import GroupUserSerializer
from radar.models import GroupUser
from radar.validation.group_users import GroupUserValidation
from radar.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView


class GroupUserListView(ListCreateModelView):
    serializer_class = GroupUserSerializer
    model_class = GroupUser
    validation_class = GroupUserValidation


class GroupUserDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = GroupUserSerializer
    model_class = GroupUser
    validation_class = GroupUserValidation


def register_views(app):
    app.add_url_rule('/group-users', view_func=GroupUserListView.as_view('group_user_list'))
    app.add_url_rule('/group-users/<int:id>', view_func=GroupUserDetailView.as_view('group_user_detail'))
