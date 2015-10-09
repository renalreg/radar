from radar_api.serializers.hospitalisations import HospitalisationSerializer
from radar.models import Hospitalisation
from radar.validation.hospitalisations import HospitalisationValidation
from radar.views.data_sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class HospitalisationListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = HospitalisationSerializer
    model_class = Hospitalisation
    validation_class = HospitalisationValidation


class HospitalisationDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = HospitalisationSerializer
    model_class = Hospitalisation
    validation_class = HospitalisationValidation
