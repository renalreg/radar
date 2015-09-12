from radar.api.serializers.plasmapheresis import PlasmapheresisSerializer
from radar.lib.models import Plasmapheresis
from radar.lib.validation.plasmapheresis import PlasmapheresisValidation
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
