from radar_api.serializers.cohorts import CohortReferenceField
from radar_api.serializers.organisations import OrganisationReferenceField
from radar.serializers.core import Serializer
from radar.serializers.fields import DateField, IntegerField, ListField


class DataPointSerializer(Serializer):
    date = DateField()
    newPatients = IntegerField()
    totalPatients = IntegerField()


class DataPointsSerializer(Serializer):
    points = ListField(DataPointSerializer())


class CohortRecruitmentRequestSerializer(Serializer):
    cohort = CohortReferenceField()


class OrganisationRecruitmentRequestSerializer(Serializer):
    organisation = OrganisationReferenceField()
