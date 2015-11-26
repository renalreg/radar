from flask import request
from sqlalchemy import or_
from sqlalchemy.sql.expression import null
from radar_api.serializers.results import ResultGroupSpecSerializer, ResultGroupSerializer, ResultGroupRequestSerializer, \
    ResultSpecSerializer, ResultGroupResultSpecSerializer
from radar.models import ResultGroupSpec, ResultGroup, ResultSpec, ResultGroupResultSpec
from radar.validation.result_groups import ResultGroupValidation
from radar.views.core import ListModelView
from radar.views.data_sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectListView, PatientObjectDetailView


# TODO should probably enforce specifying a patient here to avoid DOS
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
            query = query.filter(or_(*[ResultGroup.results[x].astext != null() for x in result_codes]))

        return query


class ResultGroupDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = ResultGroupSerializer
    model_class = ResultGroup
    validation_class = ResultGroupValidation


class ResultGroupSpecListView(ListModelView):
    serializer_class = ResultGroupSpecSerializer
    model_class = ResultGroupSpec


class ResultSpecListView(ListModelView):
    serializer_class = ResultSpecSerializer
    model_class = ResultSpec


class ResultGroupResultSpecListView(ListModelView):
    serializer_class = ResultGroupResultSpecSerializer
    model_class = ResultGroupResultSpec


def register_views(app):
    app.add_url_rule('/result-groups', view_func=ResultGroupListView.as_view('result_group_list'))
    app.add_url_rule('/result-groups/<id>', view_func=ResultGroupDetailView.as_view('result_group_detail'))
    app.add_url_rule('/result-group-specs', view_func=ResultGroupSpecListView.as_view('result_group_spec_list'))
    app.add_url_rule('/result-specs', view_func=ResultSpecListView.as_view('result_spec_list'))
    app.add_url_rule('/result-group-result-specs', view_func=ResultGroupResultSpecListView.as_view('result_group_result_spec_list'))
