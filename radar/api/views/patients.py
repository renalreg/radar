from radar.lib.serializers import MetaSerializerMixin, ModelSerializer, StringField, ListField
from radar.lib.views import ListCreateApiView, RetrieveUpdateDestroyAPIView
from radar.models import Patient, UnitPatient, Unit


class UnitSerializer(MetaSerializerMixin, ModelSerializer):
    class Meta:
        model_class = Unit


class UnitPatientSerializer(MetaSerializerMixin, ModelSerializer):
    unit = UnitSerializer()

    class Meta:
        model_class = UnitPatient
        exclude = ['patient_id', 'unit_id']


class PatientSerializer(MetaSerializerMixin, ModelSerializer):
    first_name = StringField()
    last_name = StringField()
    units = ListField(field=UnitPatientSerializer(), source='unit_patients')

    class Meta:
        model_class = Patient
        fields = ['id']


class PatientList(ListCreateApiView):
    serializer_class = PatientSerializer

    def get_query(self):
        return Patient.query


class PatientDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer

    def get_query(self):
        return Patient.query
