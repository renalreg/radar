from cornflake import fields, serializers

from radar.api.permissions import AdminWritePermission, GroupPermission
from radar.api.serializers.groups import GroupSerializer
from radar.api.views.generics import (
    ListCreateModelView,
    parse_args,
    RetrieveUpdateDestroyModelView,
)
from radar.models.groups import Group, GROUP_TYPE


class GroupListRequestSerializer(serializers.Serializer):
    code = fields.StringField(required=False)
    type = fields.EnumField(GROUP_TYPE, required=False)
    is_recruitment_number_group = fields.BooleanField(required=False)
    is_transplant_centre = fields.BooleanField(required=False)
    filter_out = fields.CommaSeparatedField(required=False, child=fields.EnumField(GROUP_TYPE))


class GroupListView(ListCreateModelView):
    serializer_class = GroupSerializer
    model_class = Group
    permission_classes = [AdminWritePermission]

    def filter_query(self, query):
        query = super(GroupListView, self).filter_query(query)

        args = parse_args(GroupListRequestSerializer)

        # Filter by code
        if args['code'] is not None:
            query = query.filter(Group.code == args['code'])

        # Filter by group type
        if args['type'] is not None:
            query = query.filter(Group.type == args['type'])

        if args['is_transplant_centre'] is not None:
            query = query.filter(Group.is_transplant_centre == args['is_transplant_centre'])

        # Filter by recruitment number flag
        if args['is_recruitment_number_group'] is not None:
            query = query.filter(Group.is_recruitment_number_group == args['is_recruitment_number_group'])

            context = self.get_context()
            user = context.get('user')
            if user.is_admin:
                return query
            country_code = self.get_user_country(user)
            query = query.filter(Group.country_code == country_code)

        # Filter out unwanted group types
        if args['filter_out']:
            query = query.filter(~Group.type.in_(args['filter_out']))

        return query

    def get_user_country(self, user):
        """Return the first country for a user."""
        for group in user.groups:
            if group.type == GROUP_TYPE.HOSPITAL:
                return group.country_code
        return None


class GroupDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = GroupSerializer
    model_class = Group
    permission_classes = [AdminWritePermission, GroupPermission]


def register_views(app):
    app.add_url_rule('/groups', view_func=GroupListView.as_view('group_list'))
    app.add_url_rule('/groups/<int:id>', view_func=GroupDetailView.as_view('group_detail'))
