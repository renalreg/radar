from radar_api.serializers.medications import MedicationSerializer
from radar.models import Medication, MEDICATION_DOSE_UNITS, MEDICATION_ROUTES, MEDICATION_FREQUENCIES
from radar.validation.medications import MedicationValidation
from radar.views.codes import CodedStringListView
from radar.views.sources import SourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class MedicationListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = MedicationSerializer
    model_class = Medication
    validation_class = MedicationValidation


class MedicationDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = MedicationSerializer
    model_class = Medication
    validation_class = MedicationValidation


class MedicationDoseUnitListView(CodedStringListView):
    items = MEDICATION_DOSE_UNITS


class MedicationFrequencyListView(CodedStringListView):
    items = MEDICATION_FREQUENCIES


class MedicationRouteListView(CodedStringListView):
    items = MEDICATION_ROUTES


def register_views(app):
    app.add_url_rule('/medications', view_func=MedicationListView.as_view('medication_list'))
    app.add_url_rule('/medications/<id>', view_func=MedicationDetailView.as_view('medication_detail'))
    app.add_url_rule('/medication-dose-units', view_func=MedicationDoseUnitListView.as_view('medication_dose_unit_list'))
    app.add_url_rule('/medication-frequencies', view_func=MedicationFrequencyListView.as_view('medication_frequency_list'))
    app.add_url_rule('/medication-routes', view_func=MedicationRouteListView.as_view('medication_route_list'))
