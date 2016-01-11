from radar_api.serializers.groups import GroupReferenceField
from radar.serializers.core import Serializer
from radar.serializers.fields import DateField, IntegerField, ListField, StringField


class DataPointSerializer(Serializer):
    date = DateField()
    newPatients = IntegerField()
    totalPatients = IntegerField()


class DataPointListSerializer(Serializer):
    points = ListField(DataPointSerializer())


class RecruitmentByGroupSerializer(Serializer):
    group = GroupReferenceField()
    patientCount = IntegerField()


class RecruitmentByGroupListSerializer(Serializer):
    counts = ListField(RecruitmentByGroupSerializer())


class RecruitmentTimelineRequestSerializer(Serializer):
    group = GroupReferenceField()


class RecruitmentByGroupRequestSerializer(Serializer):
    group = GroupReferenceField()
    group_type = StringField()
