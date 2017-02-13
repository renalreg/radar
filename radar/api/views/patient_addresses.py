from radar.api.serializers.patient_addresses import PatientAddressSerializer
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView,
    StringLookupListView,
    SystemObjectViewMixin,
)
from radar.models.patient_addresses import COUNTRIES, PatientAddress


class PatientAddressListView(SystemObjectViewMixin, PatientObjectListView):
    serializer_class = PatientAddressSerializer
    model_class = PatientAddress


class PatientAddressDetailView(SystemObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientAddressSerializer
    model_class = PatientAddress


class CountryListView(StringLookupListView):
    items = COUNTRIES


def register_views(app):
    app.add_url_rule('/patient-addresses', view_func=PatientAddressListView.as_view('patient_address_list'))
    app.add_url_rule('/patient-addresses/<id>', view_func=PatientAddressDetailView.as_view('patient_address_detail'))
    app.add_url_rule('/countries', view_func=CountryListView.as_view('countries'))
