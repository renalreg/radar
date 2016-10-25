from cornflake import serializers, fields
from sqlalchemy import func

from radar.api.serializers.common import QueryPatientField
from radar.api.serializers.results import (
    ResultSerializer,
    ObservationSerializer,
    TinyResultSerializer,
    ObservationCountSerializer
)
from radar.api.views.common import (
    SourceObjectViewMixin,
    PatientObjectDetailView,
    PatientObjectViewMixin
)
from radar.api.views.generics import (
    ListModelView,
    RetrieveModelView,
    CreateModelView,
    ListView,
    parse_args
)
from radar.database import db
from radar.models.results import Result, Observation


class ObservationListRequestSerializer(serializers.Serializer):
    value_type = fields.CommaSeparatedField(required=False, child=fields.StringField())


class ResultListRequestSerializer(serializers.Serializer):
    observation_id = fields.CommaSeparatedField(required=False, child=fields.IntegerField())


class ObservationCountListRequestSerializer(serializers.Serializer):
    patient = QueryPatientField(required=False)


class ResultListView(SourceObjectViewMixin, PatientObjectViewMixin, ListModelView):
    serializer_class = TinyResultSerializer
    model_class = Result

    def filter_query(self, query):
        query = super(ResultListView, self).filter_query(query)

        args = parse_args(ResultListRequestSerializer)

        observation_ids = args['observation_id']

        # Only results for the specified observation(s)
        if observation_ids:
            query = query.filter(Result.observation_id.in_(observation_ids))

        return query


class ResultCreateView(SourceObjectViewMixin, PatientObjectViewMixin, CreateModelView):
    serializer_class = ResultSerializer
    model_class = Result


class ResultDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = ResultSerializer
    model_class = Result


class ObservationListView(ListModelView):
    serializer_class = ObservationSerializer
    model_class = Observation

    def filter_query(self, query):
        args = parse_args(ObservationListRequestSerializer)

        value_types = args['value_type']

        # Only observations with the specified value type(s)
        if value_types:
            query = query.filter(Observation.type.in_(value_types))

        return query


class ObservationDetailView(RetrieveModelView):
    serializer_class = ObservationSerializer
    model_class = Observation


class ObservationCountListView(ListView):
    """Number of results for each type of observation."""

    serializer_class = ObservationCountSerializer

    def get_object_list(self):
        args = parse_args(ObservationCountListRequestSerializer)

        patient = args['patient']

        count_query = db.session.query(
            Result.observation_id.label('observation_id'),
            func.count().label('result_count')
        )
        count_query = count_query.select_from(Result)

        if patient is not None:
            count_query = count_query.filter(Result.patient == patient)

        count_query = count_query.group_by(Result.observation_id)
        count_subquery = count_query.subquery()

        q = db.session.query(Observation, count_subquery.c.result_count)
        q = q.join(count_subquery, Observation.id == count_subquery.c.observation_id)
        q = q.order_by(Observation.id)

        results = [dict(observation=observation, count=count) for observation, count in q]

        return results


def register_views(app):
    app.add_url_rule('/results', view_func=ResultListView.as_view('result_list'))
    app.add_url_rule('/results', view_func=ResultCreateView.as_view('result_create'))
    app.add_url_rule('/results/<id>', view_func=ResultDetailView.as_view('result_detail'))
    app.add_url_rule('/observations', view_func=ObservationListView.as_view('observation_list'))
    app.add_url_rule('/observations/<id>', view_func=ObservationDetailView.as_view('observation_detail'))
    app.add_url_rule('/observation-counts', view_func=ObservationCountListView.as_view('observation_count_list'))
