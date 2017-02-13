from radar.api.permissions import (
    GroupUserCreatePermission,
    GroupUserDestroyPermission,
    GroupUserRetrievePermission,
    GroupUserUpdatePermission,
)
from radar.api.serializers.group_users import GroupUserSerializer
from radar.api.views.common import (
    filter_query_by_group,
    filter_query_by_user,
    filter_query_by_user_permissions,
)
from radar.api.views.generics import (
    CreateModelView,
    DestroyModelView,
    ListModelView,
    RetrieveModelView,
    UpdateModelView,
)
from radar.models.groups import GroupUser


class GroupUserListView(ListModelView):
    serializer_class = GroupUserSerializer
    model_class = GroupUser

    def filter_query(self, query):
        query = super(GroupUserListView, self).filter_query(query)
        query = filter_query_by_user_permissions(query, GroupUser)
        query = filter_query_by_user(query, GroupUser)
        query = filter_query_by_group(query, GroupUser)
        return query


class GroupUserCreateView(CreateModelView):
    serializer_class = GroupUserSerializer
    model_class = GroupUser
    permission_classes = [GroupUserCreatePermission]


class GroupUserRetrieveView(RetrieveModelView):
    serializer_class = GroupUserSerializer
    model_class = GroupUser
    permission_classes = [GroupUserRetrievePermission]


class GroupUserUpdateView(UpdateModelView):
    serializer_class = GroupUserSerializer
    model_class = GroupUser
    permission_classes = [GroupUserUpdatePermission]


class GroupUserDestroyView(DestroyModelView):
    model_class = GroupUser
    permission_classes = [GroupUserDestroyPermission]


def register_views(app):
    app.add_url_rule('/group-users', view_func=GroupUserListView.as_view('group_user_list'))
    app.add_url_rule('/group-users', view_func=GroupUserCreateView.as_view('group_user_create'))
    app.add_url_rule('/group-users/<int:id>', view_func=GroupUserRetrieveView.as_view('group_user_retrieve'))
    app.add_url_rule('/group-users/<int:id>', view_func=GroupUserUpdateView.as_view('group_user_update'))
    app.add_url_rule('/group-users/<int:id>', view_func=GroupUserDestroyView.as_view('group_user_destroy'))
