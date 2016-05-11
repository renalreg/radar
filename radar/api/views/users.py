from cornflake import fields, serializers
from cornflake.validators import none_if_blank

from radar.api.permissions import (
    UserRetrievePermission,
    UserCreatePermission,
    UserUpdatePermission,
    UserDestroyPermission
)
from radar.api.serializers.common import GroupField
from radar.api.serializers.users import UserSerializer
from radar.api.views.generics import (
    ListModelView,
    CreateModelView,
    RetrieveModelView,
    UpdateModelView,
    DestroyModelView,
    parse_args
)
from radar.auth.sessions import current_user
from radar.models.users import User
from radar.user_search import UserQueryBuilder


class UserListRequestSerializer(serializers.Serializer):
    id = fields.IntegerField(required=False)
    username = fields.StringField(required=False, validators=[none_if_blank()])
    email = fields.StringField(required=False, validators=[none_if_blank()])
    first_name = fields.StringField(required=False, validators=[none_if_blank()])
    last_name = fields.StringField(required=False, validators=[none_if_blank()])
    group = fields.CommaSeparatedField(required=False, child=GroupField())
    is_enabled = fields.BooleanField(required=False)
    is_admin = fields.BooleanField(required=False)
    has_logged_in = fields.BooleanField(required=False)


class UserListView(ListModelView):
    serializer_class = UserSerializer
    model_class = User

    def get_query(self):
        args = parse_args(UserListRequestSerializer)

        builder = UserQueryBuilder(current_user)

        user_id = args['id']
        username = args['username']
        email = args['email']
        first_name = args['first_name']
        last_name = args['last_name']
        groups = args['group']
        is_enabled = args['is_enabled']
        is_admin = args['is_admin']
        has_logged_in = args['has_logged_in']

        if user_id is not None:
            builder.user_id(user_id)

        if username is not None:
            builder.username(username)

        if email is not None:
            builder.email(email)

        if first_name is not None:
            builder.first_name(first_name)

        if last_name is not None:
            builder.last_name(last_name)

        for group in groups:
            builder.group(group)

        if is_enabled is not None:
            builder.is_enabled(is_enabled)

        if is_admin is not None:
            builder.is_admin(is_admin)

        if has_logged_in is not None:
            builder.has_logged_in(has_logged_in)

        sort, reverse = self.get_sort_args()

        if sort is not None:
            builder.sort(sort, reverse)

        query = builder.build()

        return query


class UserCreateView(CreateModelView):
    serializer_class = UserSerializer
    model_class = User
    permission_classes = [UserCreatePermission]


class UserRetrieveView(RetrieveModelView):
    serializer_class = UserSerializer
    model_class = User
    permission_classes = [UserRetrievePermission]


class UserUpdateView(UpdateModelView):
    serializer_class = UserSerializer
    model_class = User
    permission_classes = [UserUpdatePermission]


class UserDestroyView(DestroyModelView):
    model_class = User
    permission_classes = [UserDestroyPermission]


def register_views(app):
    app.add_url_rule('/users', view_func=UserListView.as_view('user_list'))
    app.add_url_rule('/users', view_func=UserCreateView.as_view('user_create'))
    app.add_url_rule('/users/<int:id>', view_func=UserRetrieveView.as_view('user_retrieve'))
    app.add_url_rule('/users/<int:id>', view_func=UserUpdateView.as_view('user_update'))
    app.add_url_rule('/users/<int:id>', view_func=UserDestroyView.as_view('user_destroy'))
