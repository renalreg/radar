from radar.api.serializers.medications import MedicationSerializer, MedicationDoseUnitSerializer, \
    MedicationFrequencySerializer, MedicationRouteSerializer
from radar.lib.views import PatientDataList, FacilityDataMixin, PatientDataDetail, ListView
from radar.models import Medication, MedicationDoseUnit, MedicationFrequency, MedicationRoute


class MedicationList(FacilityDataMixin, PatientDataList):
    serializer_class = MedicationSerializer
    model_class = Medication


class MedicationDetail(FacilityDataMixin, PatientDataDetail):
    serializer_class = MedicationSerializer
    model_class = Medication


class MedicationDoseUnitList(ListView):
    serializer_class = MedicationDoseUnitSerializer
    model_class = MedicationDoseUnit


class MedicationFrequencyList(ListView):
    serializer_class = MedicationFrequencySerializer
    model_class = MedicationFrequency


class MedicationRouteList(ListView):
    serializer_class = MedicationRouteSerializer
    model_class = MedicationRoute
