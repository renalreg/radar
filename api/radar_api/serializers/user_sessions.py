from radar_api.serializers.meta import MetaSerializerMixin
from radar.models.user_sessions import UserSession
from radar.serializers.models import ModelSerializer


class UserSessionSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta(object):
        model_class = UserSession
