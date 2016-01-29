from radar.serializers.models import ModelSerializer
from radar.models.logs import Log


class LogSerializer(ModelSerializer):
    class Meta(object):
        model_class = Log
