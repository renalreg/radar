from radar_api.serializers.group_users import GroupUserSerializer
from radar.models.groups import GroupUser
from radar.validation.group_users import GroupUserValidation
from radar.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView
from radar.views.users import filter_query_by_user_permissions, filter_query_by_user
from radar.views.groups import filter_query_by_group
from radar.permissions import GroupUserPermission


class GroupUserListView(ListCreateModelView):
    serializer_class = GroupUserSerializer
    model_class = GroupUser
    validation_class = GroupUserValidation
    permission_classes = [GroupUserPermission]

    def filter_query(self, query):
        query = super(GroupUserListView, self).filter_query(query)
        query = filter_query_by_user_permissions(query, GroupUser)
        query = filter_query_by_user(query, GroupUser)
        query = filter_query_by_group(query, GroupUser)
        return query


class GroupUserDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = GroupUserSerializer
    model_class = GroupUser
    validation_class = GroupUserValidation
    permission_classes = [GroupUserPermission]


def register_views(app):
    app.add_url_rule('/group-users', view_func=GroupUserListView.as_view('group_user_list'))
    app.add_url_rule('/group-users/<int:id>', view_func=GroupUserDetailView.as_view('group_user_detail'))
