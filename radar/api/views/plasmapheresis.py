from radar.api.serializers.plasmapheresis import PlasmapheresisSerializer
from radar.lib.models import Plasmapheresis, PLASMAPHERESIS_RESPONSES, PLASMAPHERESIS_NO_OF_EXCHANGES
from radar.lib.validation.plasmapheresis import PlasmapheresisValidation
from radar.lib.views.codes import CodedStringListView
from radar.lib.views.data_sources import DataSourceObjectViewMixin
from radar.lib.views.patients import PatientObjectListView, PatientObjectDetailView


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
