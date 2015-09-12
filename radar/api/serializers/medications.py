from radar.api.serializers.data_sources import DataSourceSerializerMixin
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.patients import PatientSerializerMixin
from radar.lib.serializers import ModelSerializer, CodedStringSerializer
from radar.lib.models import Medication, MEDICATION_DOSE_UNITS, MEDICATION_FREQUENCIES, MEDICATION_ROUTES


class MedicationSerializer(MetaSerializerMixin, PatientSerializerMixin, DataSourceSerializerMixin, ModelSerializer):
    dose_unit = CodedStringSerializer(MEDICATION_DOSE_UNITS)
    frequency = CodedStringSerializer(MEDICATION_FREQUENCIES)
    route = CodedStringSerializer(MEDICATION_ROUTES)

    class Meta:
        model_class = Medication
