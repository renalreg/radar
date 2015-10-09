from radar_api.serializers.family_history import FamilyHistorySerializer
from radar.models.family_history import FamilyHistory
from radar.validation.family_history import FamilyHistoryValidation
from radar.views.cohorts import CohortObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class FamilyHistoryListView(CohortObjectViewMixin, PatientObjectListView):
    serializer_class = FamilyHistorySerializer
    model_class = FamilyHistory
    validation_class = FamilyHistoryValidation


class FamilyHistoryDetailView(CohortObjectViewMixin, PatientObjectDetailView):
    serializer_class = FamilyHistorySerializer
    model_class = FamilyHistory
    validation_class = FamilyHistoryValidation
