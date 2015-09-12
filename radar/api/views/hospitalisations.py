from radar.api.serializers.hospitalisations import HospitalisationSerializer
from radar.lib.models import Hospitalisation
from radar.lib.validation.hospitalisations import HospitalisationValidation
from radar.lib.views.data_sources import DataSourceObjectViewMixin
from radar.lib.views.patients import PatientObjectDetailView, PatientObjectListView


class HospitalisationListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = HospitalisationSerializer
    model_class = Hospitalisation
    validation_class = HospitalisationValidation


class HospitalisationDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = HospitalisationSerializer
    model_class = Hospitalisation
    validation_class = HospitalisationValidation
