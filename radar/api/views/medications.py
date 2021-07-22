from radar.api.serializers.medications import CurrentMedicationSerializer, DrugSerializer, MedicationSerializer
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView,
    SourceObjectViewMixin,
    StringLookupListView
)
from radar.api.views.generics import ListModelView
from radar.models.medications import CurrentMedication, Drug, Medication, MEDICATION_DOSE_UNITS, MEDICATION_ROUTES


class MedicationListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = MedicationSerializer
    model_class = Medication


class CurrendMedicationListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = CurrentMedicationSerializer
    model_class = CurrentMedication


class MedicationDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = MedicationSerializer
    model_class = Medication


class CurrentMedicationDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = CurrentMedicationSerializer
    model_class = CurrentMedication


class MedicationDoseUnitListView(StringLookupListView):
    items = MEDICATION_DOSE_UNITS


class MedicationRouteListView(StringLookupListView):
    items = MEDICATION_ROUTES


class DrugListView(ListModelView):
    model_class = Drug
    serializer_class = DrugSerializer


def register_views(app):
    app.add_url_rule('/medications', view_func=MedicationListView.as_view('medication_list'))
    app.add_url_rule('/medications/<id>', view_func=MedicationDetailView.as_view('medication_detail'))
    app.add_url_rule(
        '/medication-dose-units',
        view_func=MedicationDoseUnitListView.as_view('medication_dose_unit_list')
    )
    app.add_url_rule('/medication-routes', view_func=MedicationRouteListView.as_view('medication_route_list'))
    app.add_url_rule('/drugs', view_func=DrugListView.as_view('drug_list'))
    app.add_url_rule('/current-medications', view_func=CurrendMedicationListView.as_view('current_medication_list'))
    app.add_url_rule(
        '/current-medications/<id>',
        view_func=CurrentMedicationDetailView.as_view('current_medication_detail')
    )
