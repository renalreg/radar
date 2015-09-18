from radar.api.serializers.patient_addresses import PatientAddressSerializer
from radar.lib.auth.sessions import current_user
from radar.lib.models import PatientAddress
from radar.lib.patient_addresses import PatientAddressProxy
from radar.lib.validation.patient_addresses import PatientAddressValidation
from radar.lib.views.data_sources import RadarObjectViewMixin
from radar.lib.views.patients import PatientObjectListView, PatientObjectDetailView


class PatientAddressListView(RadarObjectViewMixin, PatientObjectListView):
    serializer_class = PatientAddressSerializer
    model_class = PatientAddress
    validation_class = PatientAddressValidation

    def get_object_list(self):
        addresses, pagination = super(PatientAddressListView, self).get_object_list()

        # Wrap addresses in proxy object
        addresses = [PatientAddressProxy(x, current_user) for x in addresses]

        return addresses, pagination


class PatientAddressDetailView(RadarObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientAddressSerializer
    model_class = PatientAddress
    validation_class = PatientAddressValidation

    def get_object(self):
        demographics = super(PatientAddressDetailView, self).get_object()
        return PatientAddressProxy(demographics, current_user)
