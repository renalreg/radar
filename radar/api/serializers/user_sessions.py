from cornflake.sqlalchemy_orm import ModelSerializer

from radar.api.serializers.common import MetaMixin
from radar.models.user_sessions import UserSession


class UserSessionSerializer(MetaMixin, ModelSerializer):
    class Meta(object):
        model_class = UserSession
