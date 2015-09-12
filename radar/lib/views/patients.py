from flask import request

from radar.lib.patient_search import PatientQueryBuilder
from radar.lib.permissions import PatientObjectPermission
from radar.lib.serializers import Serializer, IntegerField
from radar.lib.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView
from radar.lib.auth import current_user


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
