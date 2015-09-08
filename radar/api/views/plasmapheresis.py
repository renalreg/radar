from radar.api.serializers.plasmapheresis import PlasmapheresisSerializer, PlasmapheresisResponseSerializer
from radar.lib.views import FacilityDataMixin, PatientDataList, PatientDataDetail, ListView
from radar.models import Plasmapheresis, PlasmapheresisResponse


class PlasmapheresisList(FacilityDataMixin, PatientDataList):
    serializer_class = PlasmapheresisSerializer
    model_class = Plasmapheresis


class PlasmapheresisDetail(FacilityDataMixin, PatientDataDetail):
    serializer_class = PlasmapheresisSerializer
    model_class = Plasmapheresis


class PlasmapheresisResponseList(ListView):
    serializer_class = PlasmapheresisResponseSerializer
    model_class = PlasmapheresisResponse
