from cornflake import fields, serializers
from flask import jsonify, request
from sqlalchemy import func

from radar.api.serializers.common import QueryPatientField
from radar.api.serializers.results import (
    ObservationCountSerializer,
    ObservationSerializer,
    ResultSerializer,
    TinyResultSerializer,
)
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectViewMixin,
    SourceObjectViewMixin,
)
from radar.api.views.generics import (
    CreateModelView,
    ListModelView,
    ListView,
    parse_args,
    RetrieveModelView,
)
from radar.database import db
from radar.exceptions import BadRequest
from radar.models.results import GroupObservation, Observation, Result
from radar.utils import camel_case_keys


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

    def create(self, *args, **kwargs):
        json = request.get_json()

        if json is None:
            raise BadRequest

        if 'observation' in json:
            return super(ResultCreateView, self).create()

        observations = []
        data = {}

        for observation in json.pop('observations', []):
            data = dict(json)
            data['observation'] = observation.get('observation')
            data['sent_value'] = observation.get('value')
            data['value'] = observation.get('value')
            data['date'] = observation.get('date')
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            db.session.add(obj)
            db.session.commit()

            data = serializer.data
            data = camel_case_keys(data)
            observation = data.pop('observation')
            observation['id'] = data.pop('id', None)
            observation['value'] = data.pop('value', None)
            observation['sent_value'] = data.pop('sent_value', None)
            observations.append(observation)

        data['observations'] = observations

        return jsonify(data), 200


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

    def sort_query(self, query):
        return query.outerjoin(GroupObservation).order_by('weight')


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
