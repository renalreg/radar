from cornflake import serializers
from cornflake import fields

from radar.models.groups import GROUP_TYPE
from radar.serializers.common import GroupReferenceField


class DataPointSerializer(serializers.Serializer):
    date = fields.DateField()
    new_patients = fields.IntegerField()
    total_patients = fields.IntegerField()


class DataPointListSerializer(serializers.Serializer):
    points = fields.ListField(DataPointSerializer())


class PatientsByGroupSerializer(serializers.Serializer):
    group = GroupReferenceField()
    count = fields.IntegerField()


class PatientsByGroupListSerializer(serializers.Serializer):
    counts = fields.ListField(child=PatientsByGroupSerializer())


class RecruitmentByMonthRequestSerializer(serializers.Serializer):
    group = GroupReferenceField()


class PatientsByGroupRequestSerializer(serializers.Serializer):
    group = GroupReferenceField()
    group_type = fields.EnumField(GROUP_TYPE)


class PatientsByRecruitedGroupRequestSerializer(serializers.Serializer):
    group = GroupReferenceField()
