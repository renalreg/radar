from radar_api.serializers.plasmapheresis import PlasmapheresisSerializer
from radar.models import Plasmapheresis, PLASMAPHERESIS_RESPONSES, PLASMAPHERESIS_NO_OF_EXCHANGES
from radar.validation.plasmapheresis import PlasmapheresisValidation
from radar.views.codes import CodedStringListView
from radar.views.data_sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectListView, PatientObjectDetailView


class PlasmapheresisListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = PlasmapheresisSerializer
    model_class = Plasmapheresis
    validation_class = PlasmapheresisValidation


class PlasmapheresisDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = PlasmapheresisSerializer
    model_class = Plasmapheresis
    validation_class = PlasmapheresisValidation


class PlasmapheresisResponseListView(CodedStringListView):
    items = PLASMAPHERESIS_RESPONSES


class PlasmapheresisNoOfExchangesListView(CodedStringListView):
    items = PLASMAPHERESIS_NO_OF_EXCHANGES
