from flask import request
from flask_login import current_user
from radar.api.serializers.users import UserSerializer, UserListRequestSerializer

from radar.lib.permissions import IsAuthenticated
from radar.lib.user_search import UserQueryBuilder
from radar.lib.views import ListCreateApiView, RetrieveUpdateDestroyAPIView
from radar.models import User


class UserList(ListCreateApiView):
    serializer_class = UserSerializer
    model_class = User
    sort_fields = ('id', 'username', 'email', 'first_name', 'last_name')
    permission_classes = [IsAuthenticated]

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

        if 'disease_group' in args:
            builder.disease_group(args['disease_group'])

        if 'unit' in args:
            builder.unit(args['unit'])

        query = builder.build()

        return query


class UserDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    model_class = User
