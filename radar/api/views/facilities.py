from radar.api.serializers.patients import FacilitySerializer
from radar.lib.views import ListCreateApiView, RetrieveUpdateDestroyAPIView
from radar.models import Facility


class FacilityList(ListCreateApiView):
    serializer_class = FacilitySerializer
    model_class = Facility


class FacilityDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = FacilitySerializer
    model_class = Facility
