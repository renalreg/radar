from radar.lib.serializers import UnitSerializer
from radar.lib.views import ListCreateApiView
from radar.models import Unit


class UnitList(ListCreateApiView):
    serializer_class = UnitSerializer
    model_class = Unit
