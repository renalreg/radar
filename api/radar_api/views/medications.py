from radar_api.serializers.medications import MedicationSerializer
from radar.models import Medication, MEDICATION_DOSE_UNITS, MEDICATION_ROUTES, MEDICATION_FREQUENCIES
from radar.validation.medications import MedicationValidation
from radar.views.codes import CodedStringListView
from radar.views.data_sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


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
