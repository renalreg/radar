from radar_api.serializers.groups import GroupReferenceField
from radar.serializers.fields import LabelledIntegerField, LabelledStringField
from radar.models.patients import GENDERS, ETHNICITIES
from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, DateField, IntegerField


class RecruitPatientSearchSerializer(Serializer):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    gender = LabelledIntegerField(GENDERS)
    number = StringField()
    number_group = GroupReferenceField()


class RecruitPatientSerializer(Serializer):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    gender = LabelledIntegerField(GENDERS)
    number_group = GroupReferenceField()
    number = StringField()
    ethnicity = LabelledStringField(ETHNICITIES)
    cohort_group = GroupReferenceField()
    hospital_group = GroupReferenceField()


class PatientSerializer(Serializer):
    id = IntegerField()


class RecruitPatientResultSerializer(Serializer):
    patient = PatientSerializer()
