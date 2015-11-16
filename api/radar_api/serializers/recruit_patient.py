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
    patient_number = StringField()


class RecruitPatientResultSerializer(Serializer):
    mpiid = IntegerField()
    radar_id = IntegerField()
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    gender = CodedIntegerSerializer(GENDERS)
    nhs_no = StringField()
    chi_no = StringField()


class RecruitPatientResultListSerializer(Serializer):
    results = ListField(RecruitPatientResultSerializer())


class RecruitPatientSerializer(Serializer):
    mpiid = IntegerField()
    radar_id = IntegerField()
    recruited_by_organisation = OrganisationReferenceField()
    cohort = CohortReferenceField()
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    gender = CodedIntegerSerializer(GENDERS)
    ethnicity = EthnicityCodeReferenceField()
    nhs_no = StringField()
    chi_no = StringField()
