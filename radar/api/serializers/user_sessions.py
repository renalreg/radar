from radar.api.serializers.meta import MetaSerializerMixin
from radar.lib.models.user_sessions import UserSession
from radar.lib.serializers import ModelSerializer


class UserSessionSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = UserSession
