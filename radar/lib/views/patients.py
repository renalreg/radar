from flask import request

from radar.lib.patient_search import PatientQueryBuilder, filter_by_permissions
from radar.lib.permissions import PatientObjectPermission
from radar.lib.serializers import Serializer, IntegerField
from radar.lib.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView
from radar.lib.auth.sessions import current_user


class PatientRequestSerializer(Serializer):
    patient = IntegerField()


class PatientObjectViewMixin(object):
    def get_permission_classes(self):
        permission_classes = super(PatientObjectViewMixin, self).get_permission_classes()
        permission_classes.append(PatientObjectPermission)
        return permission_classes

    def filter_query(self, query):
        query = super(PatientObjectViewMixin, self).filter_query(query)

        patients_query = PatientQueryBuilder(current_user).build().subquery()
        query = query.join(patients_query)

        serializer = PatientRequestSerializer()
        args = serializer.to_value(request.args)

        if 'patient' in args:
            model_class = self.get_model_class()
            query = query.filter(model_class.patient_id == args['patient'])

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
