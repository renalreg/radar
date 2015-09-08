from radar.lib.serializers import LookupField, ModelSerializer, MetaSerializerMixin, PatientSerializerMixin, \
    FacilitySerializerMixin
from radar.models import MedicationFrequency, MedicationRoute, MedicationDoseUnit, Medication


class MedicationDoseUnitLookupField(LookupField):
    model_class = MedicationDoseUnit


class MedicationFrequencyLookupField(LookupField):
    model_class = MedicationFrequency


class MedicationRouteLookupField(LookupField):
    model_class = MedicationRoute


class MedicationDoseUnitSerializer(ModelSerializer):
    class Meta:
        model_class = MedicationDoseUnit


class MedicationFrequencySerializer(ModelSerializer):
    class Meta:
        model_class = MedicationFrequency


class MedicationRouteSerializer(ModelSerializer):
    class Meta:
        model_class = MedicationRoute


class MedicationSerializer(MetaSerializerMixin, PatientSerializerMixin, FacilitySerializerMixin, ModelSerializer):
    dose_unit = MedicationDoseUnitSerializer(read_only=True)
    dose_unit_id = MedicationDoseUnitLookupField(write_only=True)
    frequency = MedicationFrequencySerializer(read_only=True)
    frequency_id = MedicationFrequencyLookupField(write_only=True)
    route = MedicationRouteSerializer(read_only=True)
    route_id = MedicationRouteLookupField(write_only=True)

    class Meta:
        model_class = Medication
