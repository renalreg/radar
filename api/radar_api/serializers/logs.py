from radar.serializers.models import ModelSerializer
from radar_api.serializers.meta import TinyUserSerializer
from radar.models.logs import Log


class LogSerializer(ModelSerializer):
    user = TinyUserSerializer()

    class Meta(object):
        model_class = Log
