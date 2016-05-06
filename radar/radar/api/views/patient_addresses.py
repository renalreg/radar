from radar.models.patient_addresses import PatientAddress
from radar.serializers.patient_addresses import PatientAddressSerializer
from radar.views.common import (
    RadarObjectViewMixin,
    PatientObjectListView,
    PatientObjectDetailView
)


class PatientAddressListView(RadarObjectViewMixin, PatientObjectListView):
    serializer_class = PatientAddressSerializer
    model_class = PatientAddress


class PatientAddressDetailView(RadarObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientAddressSerializer
    model_class = PatientAddress


def register_views(app):
    app.add_url_rule('/patient-addresses', view_func=PatientAddressListView.as_view('patient_address_list'))
    app.add_url_rule('/patient-addresses/<id>', view_func=PatientAddressDetailView.as_view('patient_address_detail'))
