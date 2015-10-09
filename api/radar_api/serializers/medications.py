from radar_api.serializers.data_sources import DataSourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedStringSerializer
from radar.models import Medication, MEDICATION_DOSE_UNITS, MEDICATION_FREQUENCIES, MEDICATION_ROUTES


class MedicationSerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    dose_unit = CodedStringSerializer(MEDICATION_DOSE_UNITS)
    frequency = CodedStringSerializer(MEDICATION_FREQUENCIES)
    route = CodedStringSerializer(MEDICATION_ROUTES)

    class Meta(object):
        model_class = Medication
