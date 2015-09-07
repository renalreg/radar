from radar.lib.serializers import MetaSerializerMixin, ModelSerializer
from radar.lib.views import ListCreateApiView
from radar.models import Unit


class UnitSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = Unit


class UnitList(ListCreateApiView):
    serializer_class = UnitSerializer
    model_class = Unit
