from cornflake.sqlalchemy_orm import ModelSerializer

from radar.serializers.common import TinyUserSerializer
from radar.models.logs import Log


class LogSerializer(ModelSerializer):
    user = TinyUserSerializer()

    class Meta(object):
        model_class = Log
        exclude = ['user_id']
