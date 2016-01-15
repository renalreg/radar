from radar_api.serializers.medications import MedicationSerializer, DrugSerializer
from radar.models.medications import Medication, MEDICATION_DOSE_UNITS, MEDICATION_ROUTES, MEDICATION_FREQUENCIES, Drug
from radar.validation.medications import MedicationValidation
from radar.views.codes import CodedStringListView
from radar.views.sources import SourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView
from radar.views.core import ListModelView


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


class DrugListView(ListModelView):
    model_class = Drug
    serializer_class = DrugSerializer


def register_views(app):
    app.add_url_rule('/medications', view_func=MedicationListView.as_view('medication_list'))
    app.add_url_rule('/medications/<id>', view_func=MedicationDetailView.as_view('medication_detail'))
    app.add_url_rule('/medication-dose-units', view_func=MedicationDoseUnitListView.as_view('medication_dose_unit_list'))
    app.add_url_rule('/medication-frequencies', view_func=MedicationFrequencyListView.as_view('medication_frequency_list'))
    app.add_url_rule('/medication-routes', view_func=MedicationRouteListView.as_view('medication_route_list'))
    app.add_url_rule('/drugs', view_func=DrugListView.as_view('drug_list'))
