from radar_api.serializers.family_histories import FamilyHistorySerializer
from radar.models.family_histories import FamilyHistory, RELATIONSHIPS
from radar.validation.family_histories import FamilyHistoryValidation
from radar.views.groups import GroupObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView
from radar.views.codes import CodedIntegerListView


class FamilyHistoryListView(GroupObjectViewMixin, PatientObjectListView):
    serializer_class = FamilyHistorySerializer
    model_class = FamilyHistory
    validation_class = FamilyHistoryValidation


class FamilyHistoryDetailView(GroupObjectViewMixin, PatientObjectDetailView):
    serializer_class = FamilyHistorySerializer
    model_class = FamilyHistory
    validation_class = FamilyHistoryValidation


class FamilyHistoryRelationshipListView(CodedIntegerListView):
    items = RELATIONSHIPS


def register_views(app):
    app.add_url_rule('/family-histories', view_func=FamilyHistoryListView.as_view('family_history_list'))
    app.add_url_rule('/family-histories/<id>', view_func=FamilyHistoryDetailView.as_view('family_history_detail'))
    app.add_url_rule('/family-history-relationships', view_func=FamilyHistoryRelationshipListView.as_view('family_history_relationship_list'))
