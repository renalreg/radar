from radar_api.serializers.sources import SourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer, ReferenceField
from radar.serializers.fields import LabelledStringField
from radar.models.medications import Medication, MEDICATION_DOSE_UNITS, MEDICATION_ROUTES, Drug


class ParentDrugSerializer(ModelSerializer):
    class Meta(object):
        model_class = Drug
        exclude = ['parent_drug_id']


class ParentDrugReferenceField(ReferenceField):
    model_class = Drug
    serializer_class = ParentDrugSerializer


class DrugSerializer(ModelSerializer):
    parent_drug = ParentDrugReferenceField()

    class Meta(object):
        model_class = Drug
        exclude = ['parent_drug_id']


class DrugReferenceField(ReferenceField):
    model_class = Drug
    serializer_class = DrugSerializer


class MedicationSerializer(PatientSerializerMixin, SourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    drug = DrugReferenceField()
    dose_unit = LabelledStringField(MEDICATION_DOSE_UNITS)
    route = LabelledStringField(MEDICATION_ROUTES)

    class Meta(object):
        model_class = Medication
        exclude = ['drug_id']
