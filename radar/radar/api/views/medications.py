from radar.api.serializers.medications import MedicationSerializer
from radar.lib.models import Medication, MEDICATION_DOSE_UNITS, MEDICATION_ROUTES, MEDICATION_FREQUENCIES
from radar.lib.validation.medications import MedicationValidation
from radar.lib.views.codes import CodedStringListView
from radar.lib.views.data_sources import DataSourceObjectViewMixin
from radar.lib.views.patients import PatientObjectDetailView, PatientObjectListView


class MedicationListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = MedicationSerializer
    model_class = Medication
    validation_class = MedicationValidation


class MedicationDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = MedicationSerializer
    model_class = Medication
    validation_class = MedicationValidation


class MedicationDoseUnitListView(CodedStringListView):
    items = MEDICATION_DOSE_UNITS


class MedicationFrequencyListView(CodedStringListView):
    items = MEDICATION_FREQUENCIES


class MedicationRouteListView(CodedStringListView):
    items = MEDICATION_ROUTES
