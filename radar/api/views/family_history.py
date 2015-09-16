from radar.api.serializers.family_history import FamilyHistorySerializer
from radar.lib.models.family_history import FamilyHistory
from radar.lib.validation.family_history import FamilyHistoryValidation
from radar.lib.views.patients import PatientObjectDetailView, PatientObjectListView


class FamilyHistoryListView(PatientObjectListView):
    serializer_class = FamilyHistorySerializer
    model_class = FamilyHistory
    validation_class = FamilyHistoryValidation


class FamilyHistoryDetailView(PatientObjectDetailView):
    serializer_class = FamilyHistorySerializer
    model_class = FamilyHistory
    validation_class = FamilyHistoryValidation
