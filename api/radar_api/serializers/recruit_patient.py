from radar_api.serializers.groups import GroupReferenceField
from radar.serializers.fields import LabelledIntegerField, LabelledStringField
from radar.models.patients import GENDERS, ETHNICITIES
from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, DateField, ListField


class RecruitPatientSearchSerializer(Serializer):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    number = StringField()
    number_group = GroupReferenceField()


class PatientNumberSerializer(Serializer):
    number = StringField()
    group = GroupReferenceField()


class RecruitPatientResultSerializer(Serializer):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    gender = LabelledIntegerField(GENDERS)
    patient_numbers = ListField(PatientNumberSerializer())


class RecruitPatientResultListSerializer(Serializer):
    patients = ListField(RecruitPatientResultSerializer())


class RecruitPatientSerializer(Serializer):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    gender = LabelledIntegerField(GENDERS)
    ethnicity = LabelledStringField(ETHNICITIES)
    patient_numbers = ListField(PatientNumberSerializer())
    recruited_group = GroupReferenceField()
    group = GroupReferenceField()
