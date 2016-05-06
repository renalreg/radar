from radar.models.family_histories import FamilyHistory, RELATIONSHIPS
from radar.api.serializers.family_histories import FamilyHistorySerializer
from radar.api.views.common import (
    IntegerLookupListView,
    GroupObjectViewMixin,
    PatientObjectDetailView,
    PatientObjectListView
)


class FamilyHistoryListView(GroupObjectViewMixin, PatientObjectListView):
    serializer_class = FamilyHistorySerializer
    model_class = FamilyHistory


class FamilyHistoryDetailView(GroupObjectViewMixin, PatientObjectDetailView):
    serializer_class = FamilyHistorySerializer
    model_class = FamilyHistory


class FamilyHistoryRelationshipListView(IntegerLookupListView):
    items = RELATIONSHIPS


def register_views(app):
    app.add_url_rule('/family-histories', view_func=FamilyHistoryListView.as_view('family_history_list'))
    app.add_url_rule('/family-histories/<id>', view_func=FamilyHistoryDetailView.as_view('family_history_detail'))
    app.add_url_rule('/family-history-relationships', view_func=FamilyHistoryRelationshipListView.as_view('family_history_relationship_list'))
