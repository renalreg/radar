from radar.lib.serializers import MetaSerializerMixin, ModelSerializer
from radar.models import Unit


class UnitSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = Unit
