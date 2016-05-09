from radar.api.serializers.pathology import PathologySerializer
from radar.api.views.common import (
    StringLookupListView,
    SourceObjectViewMixin,
    PatientObjectDetailView,
    PatientObjectListView
)
from radar.models.pathology import PATHOLOGY_KIDNEY_TYPES, PATHOLOGY_KIDNEY_SIDES, Pathology


class PathologyListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = PathologySerializer
    model_class = Pathology


class PathologyDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = PathologySerializer
    model_class = Pathology


class PathologyKidneyTypeListView(StringLookupListView):
    items = PATHOLOGY_KIDNEY_TYPES


class PathologyKidneySideListView(StringLookupListView):
    items = PATHOLOGY_KIDNEY_SIDES


def register_views(app):
    app.add_url_rule('/pathology', view_func=PathologyListView.as_view('pathology_list'))
    app.add_url_rule('/pathology/<id>', view_func=PathologyDetailView.as_view('pathology_detail'))
    app.add_url_rule('/pathology-kidney-types', view_func=PathologyKidneyTypeListView.as_view('pathology_kidney_type_list'))
    app.add_url_rule('/pathology-kidney-sides', view_func=PathologyKidneySideListView.as_view('pathology_kidney_side_list'))
