from radar.lib.serializers import MetaSerializerMixin, ModelSerializer, StringField
from radar.lib.views import ListCreateApiView, RetrieveUpdateDestroyAPIView
from radar.models import Patient


class PatientSerializer(MetaSerializerMixin, ModelSerializer):
    first_name = StringField()
    last_name = StringField()

    class Meta:
        model = Patient
        fields = ['id']


class PatientList(ListCreateApiView):
    serializer_class = PatientSerializer

    def get_query(self):
        return Patient.query


class PatientDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer

    def get_query(self):
        return Patient.query
