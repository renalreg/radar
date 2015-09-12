from radar.api.serializers.patient_addresses import PatientAddressSerializer
from radar.lib.models import PatientAddress
from radar.lib.validation.patient_addresses import PatientAddressValidation
from radar.lib.views.data_sources import DataSourceObjectViewMixin
from radar.lib.views.patients import PatientObjectListView, PatientObjectDetailView


class PatientAddressListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = PatientAddressSerializer
    model_class = PatientAddress
    validation_class = PatientAddressValidation


class PatientAddressDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientAddressSerializer
    model_class = PatientAddress
    validation_class = PatientAddressValidation
