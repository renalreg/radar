from flask import request

from radar.patient_search import PatientQueryBuilder, filter_by_permissions
from radar.permissions import PatientObjectPermission
from radar.serializers.core import Serializer
from radar.serializers.fields import IntegerField
from radar.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView
from radar.auth.sessions import current_user
from radar.models.patients import Patient


def filter_query_by_patient_permissions(query, model_class):
    patients_query = PatientQueryBuilder(current_user).build()
    patients_query = patients_query.filter(Patient.id == model_class.patient_id)
    query = query.filter(patients_query.exists())
    return query


def filter_query_by_patient(query, model_class):
    serializer = PatientRequestSerializer()
    args = serializer.to_value(request.args)

    if 'patient' in args:
        query = query.filter(model_class.patient_id == args['patient'])

    return query


class PatientRequestSerializer(Serializer):
    patient = IntegerField()


class PatientObjectViewMixin(object):
    def get_permission_classes(self):
        permission_classes = super(PatientObjectViewMixin, self).get_permission_classes()
        permission_classes.append(PatientObjectPermission)
        return permission_classes

    def filter_query(self, query):
        query = super(PatientObjectViewMixin, self).filter_query(query)
        model_class = self.get_model_class()
        query = filter_query_by_patient_permissions(query, model_class)
        query = filter_query_by_patient(query, model_class)
        return query


class PatientObjectListView(PatientObjectViewMixin, ListCreateModelView):
    pass


class PatientObjectDetailView(PatientObjectViewMixin, RetrieveUpdateDestroyModelView):
    pass


class DemographicsViewMixin(object):
    def filter_query(self, query):
        query = super(DemographicsViewMixin, self).filter_query(query)

        if not current_user.is_admin:
            query = query.filter(filter_by_permissions(current_user, True))

        return query
