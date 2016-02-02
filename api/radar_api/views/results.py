from flask import request
from sqlalchemy import func

from radar.models.results import Result, Observation
from radar.views.core import ListModelView, RetrieveModelView, CreateModelView, ListView
from radar.views.sources import SourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectViewMixin
from radar_api.serializers.results import ResultSerializer, ObservationSerializer,\
    ResultListRequestSerializer, ObservationListRequestSerializer, TinyResultSerializer,\
    ObservationCountSerializer, ObservationCountListRequestSerializer
from radar.validation.results import ResultValidation
from radar.database import db
from radar.roles import PERMISSION
from radar.permissions import has_permission_for_patient
from radar.exceptions import PermissionDenied
from radar.auth.sessions import current_user


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


class ObservationCountListView(ListView):
    serializer_class = ObservationCountSerializer

    def get_object_list(self):
        serializer = ObservationCountListRequestSerializer()
        args = serializer.args_to_value(request.args)

        patient = args.get('patient')

        if patient is not None and not has_permission_for_patient(current_user, patient, PERMISSION.VIEW_PATIENT):
            raise PermissionDenied()

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
