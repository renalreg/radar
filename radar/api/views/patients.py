from radar.lib.serializers import MetaSerializerMixin, ModelSerializer, StringField, ListField, DateField, IntegerField
from radar.lib.views import ListCreateApiView, RetrieveUpdateDestroyAPIView
from radar.models import Patient, UnitPatient, Unit, DiseaseGroup, DiseaseGroupPatient


class UnitSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = Unit


class UnitPatientSerializer(MetaSerializerMixin, ModelSerializer):
    unit = UnitSerializer()

    class Meta:
        model_class = UnitPatient
        exclude = ['patient_id', 'unit_id']


class DiseaseGroupSerializer(MetaSerializerMixin, ModelSerializer):
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
    gender = StringField()
    units = ListField(field=UnitPatientSerializer(), source='unit_patients')
    disease_groups = ListField(field=DiseaseGroupPatientSerializer(), source='disease_group_patients')

    class Meta:
        model_class = Patient
        fields = ['id']


class PatientList(ListCreateApiView):
    serializer_class = PatientSerializer
    sort_fields = {'first_name': Patient.first_name}

    def get_query(self):
        return Patient.query


class PatientDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer

    def get_query(self):
        return Patient.query
