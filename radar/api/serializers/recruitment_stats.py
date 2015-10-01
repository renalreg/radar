from radar.api.serializers.cohorts import CohortReferenceField
from radar.api.serializers.organisations import OrganisationReferenceField
from radar.lib.serializers.core import Serializer
from radar.lib.serializers.fields import DateField, IntegerField, ListField, BooleanField


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
