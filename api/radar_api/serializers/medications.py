from radar_api.serializers.sources import SourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer, ReferenceField
from radar.serializers.fields import LabelledStringField
from radar.models.medications import Medication, MEDICATION_DOSE_UNITS, MEDICATION_FREQUENCIES, MEDICATION_ROUTES, Drug


class DrugSerializer(ModelSerializer):
    class Meta(object):
        model_class = Drug


class DrugReferenceField(ReferenceField):
    model_class = Drug
    serializer_class = DrugSerializer


class MedicationSerializer(PatientSerializerMixin, SourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    drug = DrugReferenceField()
    dose_unit = LabelledStringField(MEDICATION_DOSE_UNITS)
    frequency = LabelledStringField(MEDICATION_FREQUENCIES)
    route = LabelledStringField(MEDICATION_ROUTES)

    class Meta(object):
        model_class = Medication
        exclude = ['drug_id']
