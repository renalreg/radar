from flask import request

from radar.validation.users import UserValidation
from radar_api.serializers.users import UserSerializer, UserListRequestSerializer
from radar.user_search import UserQueryBuilder
from radar.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView
from radar.models import User
from radar.auth.sessions import current_user, logout_other_sessions, logout_user
from radar.permissions import UserListPermission, UserDetailPermission
from radar.database import db


class UserListView(ListCreateModelView):
    serializer_class = UserSerializer
    validation_class = UserValidation
    model_class = User
    permission_classes = [UserListPermission]
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


class UserDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = UserSerializer
    validation_class = UserValidation
    model_class = User
    permission_classes = [UserDetailPermission]

    def get_context(self, deserialized_data):
        ctx = super(UserDetailView, self).get_context(deserialized_data)
        ctx['current_password'] = deserialized_data.get('current_password')
        return ctx

    def update(self, *args, **kwargs):
        obj = self.get_object()
        old_password_hash = obj.password_hash
        old_email = obj.email

        r = super(UserDetailView, self).update(*args, **kwargs)

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
    app.add_url_rule('/users/<int:id>', view_func=UserDetailView.as_view('user_detail'))
