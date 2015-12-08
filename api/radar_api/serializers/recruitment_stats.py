from radar_api.serializers.cohorts import CohortReferenceField
from radar_api.serializers.organisations import OrganisationReferenceField
from radar.serializers.core import Serializer
from radar.serializers.fields import DateField, IntegerField, ListField


class DataPointSerializer(Serializer):
    date = DateField()
    newPatients = IntegerField()
    totalPatients = IntegerField()


class DataPointListSerializer(Serializer):
    points = ListField(DataPointSerializer())


class CohortRecruitmentRequestSerializer(Serializer):
    cohort = CohortReferenceField()


class OrganisationRecruitmentRequestSerializer(Serializer):
    organisation = OrganisationReferenceField()


class RecruitmentByCohortRequestSerializer(Serializer):
    organisation = OrganisationReferenceField()


class RecruitmentByOrganisationRequestSerializer(Serializer):
    cohort = CohortReferenceField()


class RecruitByCohortSerializer(Serializer):
    cohort = CohortReferenceField()
    patientCount = IntegerField()


class RecruitByCohortListSerializer(Serializer):
    counts = ListField(RecruitByCohortSerializer())


class RecruitByOrganisationSerializer(Serializer):
    organisation = OrganisationReferenceField()
    patientCount = IntegerField()


class RecruitByOrganisationListSerializer(Serializer):
    counts = ListField(RecruitByOrganisationSerializer())
