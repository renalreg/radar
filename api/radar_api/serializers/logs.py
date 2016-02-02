from radar.serializers.models import ModelSerializer
from radar_api.serializers.meta import TinyUserSerializer
from radar.serializers.fields import IntegerField, StringField, DateTimeField
from radar.serializers.core import Serializer
from radar.models.logs import Log


class LogSerializer(ModelSerializer):
    user = TinyUserSerializer()

    class Meta(object):
        model_class = Log


class LogListRequestSerializer(Serializer):
    from_date = DateTimeField()
    to_date = DateTimeField()
    type = StringField()
    user = IntegerField()
    patient = IntegerField()
    table_name = StringField()
