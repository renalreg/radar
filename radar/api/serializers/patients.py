from radar.lib.serializers import ModelSerializer, ListField, MetaSerializerMixin, StringField, DateField, IntegerField, \
    LookupField, Serializer, BooleanField
from radar.models import Facility, Unit, UnitPatient, DiseaseGroupFeature, DiseaseGroup, DiseaseGroupPatient, Patient


class FacilitySerializer(ModelSerializer):
    class Meta:
        model_class = Facility


class UnitSerializer(ModelSerializer):
    facilities = ListField(field=FacilitySerializer())

    class Meta:
        model_class = Unit


class UnitPatientSerializer(MetaSerializerMixin, ModelSerializer):
    unit = UnitSerializer()

    class Meta:
        model_class = UnitPatient
        exclude = ['patient_id', 'unit_id']


class DiseaseGroupFeatureSerializer(ModelSerializer):
    class Meta:
        model_class = DiseaseGroupFeature


class DiseaseGroupSerializer(MetaSerializerMixin, ModelSerializer):
    features = ListField(field=DiseaseGroupFeatureSerializer(), source='disease_group_features')

    class Meta:
        model_class = DiseaseGroup


class DiseaseGroupPatientSerializer(MetaSerializerMixin, ModelSerializer):
    disease_group = DiseaseGroupSerializer()

    class Meta:
        model_class = DiseaseGroupPatient
        exclude = ['patient_id', 'disease_group_id']


class PatientSerializer(MetaSerializerMixin, ModelSerializer):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    year_of_birth = IntegerField()
    gender = StringField()
    units = ListField(field=UnitPatientSerializer(), source='unit_patients')
    disease_groups = ListField(field=DiseaseGroupPatientSerializer(), source='disease_group_patients')

    class Meta:
        model_class = Patient
        fields = ['id']


class DiseaseGroupLookupField(LookupField):
    model_class = DiseaseGroup


class UnitLookupField(LookupField):
    model_class = Unit


class PatientListRequestSerializer(Serializer):
    id = IntegerField()
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    year_of_birth = IntegerField()
    date_of_death = DateField()
    year_of_death = IntegerField()
    gender = StringField()
    patient_number = StringField()
    unit_id = UnitLookupField(write_only=True)
    disease_group_id = DiseaseGroupLookupField(write_only=True)
    is_active = BooleanField()
