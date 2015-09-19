from radar.lib.models import ResultSpec, ResultGroupSpec
from radar.lib.serializers import ModelSerializer, ListField


class ResultSpecSerializer(ModelSerializer):
    class Meta(object):
        model_class = ResultSpec


class ResultGroupSpecSerializer(ModelSerializer):
    result_specs = ListField(ResultSpecSerializer())

    class Meta(object):
        model_class = ResultGroupSpec
