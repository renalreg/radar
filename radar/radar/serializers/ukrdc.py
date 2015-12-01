from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, DateTimeField, ListField, IntegerField


class NameSerializer(Serializer):
    given = StringField()
    family = StringField()


class NumberSerializer(Serializer):
    number = StringField()
    code_system = StringField()


class SearchSerializer(Serializer):
    name = NameSerializer()
    birth_time = DateTimeField()
    patient_number = NumberSerializer()


class ResultSerializer(Serializer):
    name = NameSerializer()
    birth_time = DateTimeField()
    gender = IntegerField()
    patient_numbers = ListField(NumberSerializer())


class ResultListSerializer(Serializer):
    patients = ListField(ResultSerializer())
