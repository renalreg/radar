from radar_api.serializers.groups import GroupReferenceField
from radar.serializers.core import Serializer
from radar.serializers.fields import DateField, IntegerField, ListField


class DataPointSerializer(Serializer):
    date = DateField()
    newPatients = IntegerField()
    totalPatients = IntegerField()


class DataPointListSerializer(Serializer):
    points = ListField(DataPointSerializer())


class GroupRecruitmentRequestSerializer(Serializer):
    group = GroupReferenceField()


class RecruitmentByGroupRequestSerializer(Serializer):
    group = GroupReferenceField()


class RecruitmentByGroupSerializer(Serializer):
    group = GroupReferenceField()
    patientCount = IntegerField()


class RecruitmentByGroupListSerializer(Serializer):
    counts = ListField(RecruitmentByGroupSerializer())
