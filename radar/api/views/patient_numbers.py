from radar.api.serializers.patient_numbers import PatientNumberSerializer
from radar.lib.auth import current_user
from radar.lib.models import PatientNumber
from radar.lib.patient_search import filter_by_permissions
from radar.lib.validation.patient_numbers import PatientNumberValidation
from radar.lib.views.data_sources import RadarObjectViewMixin
from radar.lib.views.patients import PatientObjectDetailView, PatientObjectListView


class PatientNumberListView(RadarObjectViewMixin, PatientObjectListView):
    serializer_class = PatientNumberSerializer
    model_class = PatientNumber
    validation_class = PatientNumberValidation

    def filter_query(self, query):
        query = query.filter(filter_by_permissions(current_user, True))
        return query


class PatientNumberDetailView(RadarObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientNumberSerializer
    model_class = PatientNumber
    validation_class = PatientNumberValidation

    def filter_query(self, query):
        query = query.filter(filter_by_permissions(current_user, True))
        return query
