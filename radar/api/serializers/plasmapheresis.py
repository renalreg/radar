from radar.lib.serializers import LookupField, ModelSerializer, MetaSerializerMixin, PatientSerializerMixin, \
    FacilitySerializerMixin, DateField, StringField, FloatField
from radar.models import MedicationFrequency, MedicationRoute, MedicationDoseUnit, Medication, Plasmapheresis, \
    PlasmapheresisResponse


class PlasmapheresisResponseLookupField(LookupField):
    model_class = PlasmapheresisResponse


class PlasmapheresisResponseSerializer(ModelSerializer):
    class Meta:
        model_class = PlasmapheresisResponse


class PlasmapheresisSerializer(MetaSerializerMixin, PatientSerializerMixin, FacilitySerializerMixin, ModelSerializer):
    response = PlasmapheresisResponseSerializer(read_only=True)
    response_id = PlasmapheresisResponseLookupField(write_only=True)

    class Meta:
        model_class = Plasmapheresis
