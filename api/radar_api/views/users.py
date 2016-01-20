from flask import request

from radar.validation.users import UserValidation
from radar_api.serializers.users import UserSerializer, UserListRequestSerializer
from radar.user_search import UserQueryBuilder
from radar.views.core import ListModelView, CreateModelView, RetrieveModelView, UpdateModelView
from radar.models.users import User
from radar.auth.sessions import current_user, logout_other_sessions, logout_user
from radar.permissions import UserRetrievePermission, UserCreatePermission, UserUpdatePermission
from radar.database import db


class UserListView(ListModelView):
    serializer_class = UserSerializer
    validation_class = UserValidation
    model_class = User
    sort_fields = ('id', 'username', 'email', 'first_name', 'last_name')

    def get_query(self):
        serializer = UserListRequestSerializer()
        args = serializer.args_to_value(request.args)

        builder = UserQueryBuilder(current_user)

        if args.get('id') is not None:
            builder.user_id(args['id'])

        if args.get('username'):
            builder.username(args['username'])

        if args.get('email'):
            builder.email(args['email'])

        if args.get('first_name'):
            builder.first_name(args['first_name'])

        if args.get('last_name'):
            builder.last_name(args['last_name'])

        groups = args.get('group', [])

        for group in groups:
            builder.group(group)

        query = builder.build()

        return query


class UserCreateView(CreateModelView):
    serializer_class = UserSerializer
    validation_class = UserValidation
    model_class = User
    permission_classes = [UserCreatePermission]


class UserRetrieveView(RetrieveModelView):
    serializer_class = UserSerializer
    model_class = User
    permission_classes = [UserRetrievePermission]


class UserUpdateView(UpdateModelView):
    serializer_class = UserSerializer
    validation_class = UserValidation
    model_class = User
    permission_classes = [UserUpdatePermission]

    def get_context(self, deserialized_data):
        ctx = super(UserUpdateView, self).get_context(deserialized_data)
        ctx['current_password'] = deserialized_data.get('current_password')
        return ctx

    def update(self, *args, **kwargs):
        obj = self.get_object()
        old_password_hash = obj.password_hash
        old_email = obj.email

        r = super(UserUpdateView, self).update(*args, **kwargs)

        # Changed password or email
        if obj.password_hash != old_password_hash or obj.email != old_email:
            # User changed their own password
            if current_user == obj:
                logout_other_sessions()
            else:
                logout_user(obj)
                db.session.commit()

        return r


def register_views(app):
    app.add_url_rule('/users', view_func=UserListView.as_view('user_list'))
    app.add_url_rule('/users', view_func=UserCreateView.as_view('user_create'))
    app.add_url_rule('/users/<int:id>', view_func=UserRetrieveView.as_view('user_retrieve'))
    app.add_url_rule('/users/<int:id>', view_func=UserUpdateView.as_view('user_update'))
