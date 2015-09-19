from radar.lib.models import ResultSpec, ResultGroupSpec
from radar.lib.serializers import ModelSerializer, ListField


class ResultSpecSerializer(ModelSerializer):
    class Meta(object):
        model_class = ResultSpec
        exclude = ['result_select_id']


class ResultGroupSpecSerializer(ModelSerializer):
    results = ListField(ResultSpecSerializer(), source='sorted_results')

    class Meta(object):
        model_class = ResultGroupSpec
