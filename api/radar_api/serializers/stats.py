from radar_api.serializers.groups import GroupReferenceField
from radar.serializers.core import Serializer
from radar.serializers.fields import DateField, IntegerField, ListField, EnumField
from radar.models.groups import GROUP_TYPE


class DataPointSerializer(Serializer):
    date = DateField()
    newPatients = IntegerField()
    totalPatients = IntegerField()


class DataPointListSerializer(Serializer):
    points = ListField(DataPointSerializer())


class PatientsByGroupSerializer(Serializer):
    group = GroupReferenceField()
    count = IntegerField()


class PatientsByGroupListSerializer(Serializer):
    counts = ListField(PatientsByGroupSerializer())


class RecruitmentByMonthRequestSerializer(Serializer):
    group = GroupReferenceField()


class PatientsByGroupRequestSerializer(Serializer):
    group = GroupReferenceField()
    group_type = EnumField(GROUP_TYPE)


class PatientsByRecruitedGroupRequestSerializer(Serializer):
    group = GroupReferenceField()
