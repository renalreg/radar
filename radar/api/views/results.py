from flask import request
from sqlalchemy import or_
from radar.api.serializers.results import ResultGroupSpecSerializer, ResultGroupSerializer, ResultGroupRequestSerializer, \
    ResultSpecSerializer
from radar.lib.models import ResultGroupSpec, ResultGroup, ResultSpec
from radar.lib.validation.result_groups import ResultGroupValidation
from radar.lib.views.core import ListModelView
from radar.lib.views.data_sources import DataSourceObjectViewMixin
from radar.lib.views.patients import PatientObjectListView, PatientObjectDetailView


class ResultGroupSpecListView(ListModelView):
    serializer_class = ResultGroupSpecSerializer
    model_class = ResultGroupSpec


class ResultSpecListView(ListModelView):
    serializer_class = ResultSpecSerializer
    model_class = ResultSpec


class ResultGroupDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = ResultGroupSerializer
    model_class = ResultGroup
    validation_class = ResultGroupValidation


class ResultGroupListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = ResultGroupSerializer
    model_class = ResultGroup
    validation_class = ResultGroupValidation

    def filter_query(self, query):
        query = super(ResultGroupListView, self).filter_query(query)

        serializer = ResultGroupRequestSerializer()
        args = serializer.args_to_value(request.args)

        if 'result_group_codes' in args:
            result_group_codes = args['result_group_codes']
            query = query.join(ResultGroup.result_group_spec)
            query = query.filter(or_(*[ResultGroup.code == x for x in result_group_codes]))

        if 'result_codes' in args:
            result_codes = args['result_codes']
            query = query.filter(or_(*[ResultGroup.results[x].astext != None for x in result_codes]))

        print query

        return query
