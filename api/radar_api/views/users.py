from flask import request

from radar.validation.users import UserValidation
from radar_api.serializers.users import UserSerializer, UserListRequestSerializer
from radar.user_search import UserQueryBuilder
from radar.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView
from radar.models import User
from radar.auth.sessions import current_user
from radar.permissions import UserListPermission, UserDetailPermission


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

        if args.get('cohort') is not None:
            builder.cohort(args['cohort'])

        if args.get('organisation') is not None:
            builder.organisation(args['organisation'])

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


def register_views(app):
    app.add_url_rule('/users', view_func=UserListView.as_view('user_list'))
    app.add_url_rule('/users/<int:id>', view_func=UserDetailView.as_view('user_detail'))
