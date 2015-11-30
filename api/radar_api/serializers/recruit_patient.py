from radar_api.serializers.patient_demographics import EthnicityCodeReferenceField
from radar_api.serializers.cohorts import CohortReferenceField
from radar_api.serializers.organisations import OrganisationReferenceField
from radar.serializers.codes import CodedIntegerSerializer
from radar.models.patients import GENDERS
from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, IntegerField, DateField, ListField


class RecruitPatientSearchSerializer(Serializer):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    number = StringField()
    number_organisation = OrganisationReferenceField()


class PatientNumberSerializer(Serializer):
    number = StringField()
    organisation = OrganisationReferenceField()


class RecruitPatientResultSerializer(Serializer):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    gender = CodedIntegerSerializer(GENDERS)
    patient_numbers = ListField(PatientNumberSerializer())


class RecruitPatientResultListSerializer(Serializer):
    patients = ListField(RecruitPatientResultSerializer())


class RecruitPatientSerializer(Serializer):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    gender = CodedIntegerSerializer(GENDERS)
    ethnicity = EthnicityCodeReferenceField()
    patient_numbers = ListField(PatientNumberSerializer())
    recruited_by_organisation = OrganisationReferenceField()
    cohort = CohortReferenceField()
