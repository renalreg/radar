from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, DateTimeField, IntegerField, ListField


class PatientNameSerializer(Serializer):
    given = StringField()
    family = StringField()


class PatientNumberSerializer(Serializer):
    number = StringField()
    code_system = StringField()


class PatientSearchSerializer(Serializer):
    name = PatientNameSerializer()
    birth_time = DateTimeField()
    patient_number = PatientNumberSerializer()


class PatientResultSerializer(Serializer):
    name = PatientNameSerializer()
    birth_time = DateTimeField()
    gender = StringField()
    patient_numbers = ListField(PatientNumberSerializer())


class PatientResultListSerializer(Serializer):
    patients = ListField(PatientResultSerializer())
