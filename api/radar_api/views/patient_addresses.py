from radar_api.serializers.patient_addresses import PatientAddressSerializer
from radar.auth.sessions import current_user
from radar.models import PatientAddress
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


def register_views(app):
    app.add_url_rule('/patient-addresses', view_func=PatientAddressListView.as_view('patient_address_list'))
    app.add_url_rule('/patient-addresses/<id>', view_func=PatientAddressDetailView.as_view('patient_address_detail'))
