from flask import request

from radar.models.results import Result, Observation
from radar.views.core import ListModelView, RetrieveModelView, CreateModelView
from radar.views.sources import SourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectViewMixin
from radar_api.serializers.results import ResultSerializer, ObservationSerializer,\
    ResultListRequestSerializer, ObservationListRequestSerializer, TinyResultSerializer
from radar.validation.results import ResultValidation


class ResultListView(SourceObjectViewMixin, PatientObjectViewMixin, ListModelView):
    serializer_class = TinyResultSerializer
    model_class = Result
    validation_class = ResultValidation

    def filter_query(self, query):
        query = super(ResultListView, self).filter_query(query)

        serializer = ResultListRequestSerializer()
        args = serializer.args_to_value(request.args)

        observation_ids = args.get('observation_ids')

        if observation_ids:
            query = query.filter(Result.observation_id.in_(observation_ids))

        return query


class ResultCreateView(SourceObjectViewMixin, PatientObjectViewMixin, CreateModelView):
    serializer_class = ResultSerializer
    model_class = Result
    validation_class = ResultValidation


class ResultDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = ResultSerializer
    model_class = Result
    validation_class = ResultValidation


class ObservationListView(ListModelView):
    serializer_class = ObservationSerializer
    model_class = Observation

    def filter_query(self, query):
        serializer = ObservationListRequestSerializer()
        args = serializer.args_to_value(request.args)

        if 'value_type' in args:
            query = query.filter(Observation.type == args['value_type'])

        if 'value_types' in args:
            query = query.filter(Observation.type.in_(args['value_types']))

        return query


class ObservationDetailView(RetrieveModelView):
    serializer_class = ObservationSerializer
    model_class = Observation


def register_views(app):
    app.add_url_rule('/results', view_func=ResultListView.as_view('result_list'))
    app.add_url_rule('/results', view_func=ResultCreateView.as_view('result_create'))
    app.add_url_rule('/results/<id>', view_func=ResultDetailView.as_view('result_detail'))
    app.add_url_rule('/observations', view_func=ObservationListView.as_view('observation_list'))
    app.add_url_rule('/observations/<id>', view_func=ObservationDetailView.as_view('observation_detail'))
