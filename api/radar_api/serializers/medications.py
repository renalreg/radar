from radar_api.serializers.sources import SourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.fields import LabelledStringField
from radar.models import Medication, MEDICATION_DOSE_UNITS, MEDICATION_FREQUENCIES, MEDICATION_ROUTES


class MedicationSerializer(PatientSerializerMixin, SourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    dose_unit = LabelledStringField(MEDICATION_DOSE_UNITS)
    frequency = LabelledStringField(MEDICATION_FREQUENCIES)
    route = LabelledStringField(MEDICATION_ROUTES)

    class Meta(object):
        model_class = Medication
