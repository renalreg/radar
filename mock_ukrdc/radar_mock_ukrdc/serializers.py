from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, DateField, IntegerField, ListField


class PatientSearchSerializer(Serializer):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()


class PatientResultSerializer(Serializer):
    mpiid = IntegerField()
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()


class PatientResultListSerializer(Serializer):
    results = ListField(PatientResultSerializer())
