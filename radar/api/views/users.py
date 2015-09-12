from flask import request

from radar.api.serializers.users import UserSerializer, UserListRequestSerializer
from radar.lib.user_search import UserQueryBuilder
from radar.lib.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView
from radar.lib.models import User
from radar.lib.auth import current_user


class UserListView(ListCreateModelView):
    serializer_class = UserSerializer
    model_class = User
    sort_fields = ('id', 'username', 'email', 'first_name', 'last_name')

    def get_query(self):
        serializer = UserListRequestSerializer()
        args = serializer.args_to_value(request.args)

        builder = UserQueryBuilder(current_user)

        if 'id' in args:
            builder.user_id(args['id'])

        if 'username' in args:
            builder.username(args['username'])

        if 'email' in args:
            builder.email(args['email'])

        if 'first_name' in args:
            builder.first_name(args['first_name'])

        if 'last_name' in args:
            builder.last_name(args['last_name'])

        if 'cohort' in args:
            builder.cohort(args['cohort'])

        if 'organisation' in args:
            builder.organisation(args['organisation'])

        query = builder.build()

        return query


class UserDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = UserSerializer
    model_class = User
