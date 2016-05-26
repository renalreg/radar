from cornflake import fields, serializers

from radar.api.permissions import AdminWritePermission
from radar.api.serializers.groups import GroupSerializer
from radar.api.views.generics import (
    ListCreateModelView,
    RetrieveUpdateDestroyModelView,
    parse_args
)
from radar.models.groups import Group, GROUP_TYPE


class GroupListRequestSerializer(serializers.Serializer):
    code = fields.StringField(required=False)
    type = fields.EnumField(GROUP_TYPE, required=False)
    is_recruitment_number_group = fields.BooleanField(required=False)


class GroupListView(ListCreateModelView):
    serializer_class = GroupSerializer
    model_class = Group
    permission_classes = [AdminWritePermission]

    def filter_query(self, query):
        query = super(GroupListView, self).filter_query(query)

        args = parse_args(GroupListRequestSerializer)

        if args['code'] is not None:
            query = query.filter(Group.code == args['code'])

        if args['type'] is not None:
            query = query.filter(Group.type == args['type'])

        if args['is_recruitment_number_group'] is not None:
            query = query.filter(Group.is_recruitment_number_group == args['is_recruitment_number_group'])

        return query


class GroupDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = GroupSerializer
    model_class = Group
    permission_classes = [AdminWritePermission]


def register_views(app):
    app.add_url_rule('/groups', view_func=GroupListView.as_view('group_list'))
    app.add_url_rule('/groups/<int:id>', view_func=GroupDetailView.as_view('group_detail'))
