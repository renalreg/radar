from radar_api.serializers.patient_addresses import PatientAddressSerializer
from radar.auth.sessions import current_user
from radar.models import PatientAddress
from radar.patient_addresses import PatientAddressProxy
from radar.validation.patient_addresses import PatientAddressValidation
from radar.views.data_sources import RadarObjectViewMixin
from radar.views.patients import PatientObjectListView, PatientObjectDetailView


class PatientAddressListView(RadarObjectViewMixin, PatientObjectListView):
    serializer_class = PatientAddressSerializer
    model_class = PatientAddress
    validation_class = PatientAddressValidation

    def get_serializer(self):
        return PatientAddressSerializer(current_user)


class PatientAddressDetailView(RadarObjectViewMixin, PatientObjectDetailView):
    model_class = PatientAddress
    validation_class = PatientAddressValidation

    def get_serializer(self):
        return PatientAddressSerializer(current_user)
