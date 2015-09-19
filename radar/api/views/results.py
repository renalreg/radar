from flask import request
from radar.api.serializers.results import ResultGroupSpecSerializer, ResultGroupSerializer, ResultGroupRequestSerializer
from radar.lib.models import ResultGroupSpec, ResultGroup
from radar.lib.validation.result_groups import ResultGroupValidation
from radar.lib.views.core import ListModelView
from radar.lib.views.data_sources import DataSourceObjectViewMixin
from radar.lib.views.patients import PatientObjectListView


class ResultGroupSpecListView(ListModelView):
    serializer_class = ResultGroupSpecSerializer
    model_class = ResultGroupSpec


class ResultGroupListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = ResultGroupSerializer
    model_class = ResultGroup
    validation_class = ResultGroupValidation

    def filter_query(self, query):
        query = super(ResultGroupListView, self).filter_query(query)

        serializer = ResultGroupRequestSerializer()
        args = serializer.args_to_value(request.args)

        if 'result_group_code' in args:
            query = query.join(ResultGroup.result_group_spec).filter(ResultGroupSpec.code == args['result_group_code'])

        return query
