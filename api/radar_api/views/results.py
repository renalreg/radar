from flask import request

from radar.models.results import Result, Observation
from radar.views.core import ListModelView, RetrieveModelView
from radar.views.sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectListView, PatientObjectDetailView
from radar_api.serializers.results import ResultSerializer, ObservationSerializer,\
    ResultListRequestSerializer, ObservationListRequestSerializer
from radar.validation.results import ResultValidation


class ResultListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = ResultSerializer
    model_class = Result
    validation_class = ResultValidation

    def filter_query(self, query):
        serializer = ResultListRequestSerializer()
        args = serializer.args_to_value(request.args)

        if 'observation_id' in args:
            query = query.filter(Result.observation_id == args['observation_id'])

        if 'observation_ids' in args:
            query = query.filter(Result.observation_id.in_(args['observation_ids']))

        return query


class ResultDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = ResultSerializer
    model_class = Result
    validation_class = ResultValidation


class ObservationListView(ListModelView):
    serializer_class = ObservationSerializer
    model_class = Observation

    def filter_query(self, query):
        serializer = ObservationListRequestSerializer()
        args = serializer.args_to_value(request.args)

        if 'type' in args:
            query = query.filter(Observation.type == args['type'])

        if 'types' in args:
            query = query.filter(Observation.type.in_(args['types']))

        return query


class ObservationDetailView(RetrieveModelView):
    serializer_class = ObservationSerializer
    model_class = Observation


def register_views(app):
    app.add_url_rule('/results', view_func=ResultListView.as_view('result_list'))
    app.add_url_rule('/results/<id>', view_func=ResultDetailView.as_view('result_detail'))
    app.add_url_rule('/observations', view_func=ObservationListView.as_view('observation_list'))
    app.add_url_rule('/observations/<id>', view_func=ObservationDetailView.as_view('observation_detail'))
