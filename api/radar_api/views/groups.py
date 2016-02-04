from flask import request

from radar_api.serializers.groups import GroupSerializer, GroupListRequestSerializer
from radar.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView
from radar.models.groups import Group
from radar.permissions import AdminWritePermission
from radar.validation.groups import GroupValidation


class GroupListView(ListCreateModelView):
    serializer_class = GroupSerializer
    model_class = Group
    validation_class = GroupValidation
    permission_classes = [AdminWritePermission]

    def filter_query(self, query):
        query = super(GroupListView, self).filter_query(query)

        serializer = GroupListRequestSerializer()
        args = serializer.args_to_value(request.args)

        if 'code' in args:
            query = query.filter(Group.code == args['code'])

        if 'type' in args:
            query = query.filter(Group.type == args['type'])

        if 'is_recruitment_group' in args:
            query = query.filter(Group.is_recruitment_group == args['is_recruitment_group'])

        if 'is_recruitment_number_group' in args:
            query = query.filter(Group.is_recruitment_number_group == args['is_recruitment_number_group'])

        return query


class GroupDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = GroupSerializer
    model_class = Group
    validation_class = GroupValidation
    permission_classes = [AdminWritePermission]


def register_views(app):
    app.add_url_rule('/groups', view_func=GroupListView.as_view('group_list'))
    app.add_url_rule('/groups/<int:id>', view_func=GroupDetailView.as_view('group_detail'))
