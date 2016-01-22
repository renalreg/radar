from flask import request

from radar.serializers.core import Serializer
from radar.serializers.fields import IntegerField
from radar.user_search import UserQueryBuilder
from radar.auth.sessions import current_user
from radar.models.users import User


def filter_query_by_user_permissions(query, model_class):
    users_query = UserQueryBuilder(current_user).build()
    users_query = users_query.filter(User.id == model_class.user_id)
    query = query.filter(users_query.exists())
    return query


def filter_query_by_user(query, model_class):
    serializer = UserRequestSerializer()
    args = serializer.to_value(request.args)

    if 'user' in args:
        query = query.filter(model_class.user_id == args['user'])

    return query


class UserRequestSerializer(Serializer):
    user = IntegerField()
