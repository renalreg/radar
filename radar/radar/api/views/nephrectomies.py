from radar.models.nephrectomies import Nephrectomy, NEPHRECTOMY_KIDNEY_SIDES, NEPHRECTOMY_KIDNEY_TYPES, NEPHRECTOMY_ENTRY_TYPES
from radar.serializers.nephrectomies import NephrectomySerializer
from radar.views.common import (
    StringLookupListView,
    SourceObjectViewMixin,
    PatientObjectDetailView,
    PatientObjectListView
)


class NephrectomyListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = NephrectomySerializer
    model_class = Nephrectomy


class NephrectomyDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = NephrectomySerializer
    model_class = Nephrectomy


class NephrectomyKidneySideListView(StringLookupListView):
    items = NEPHRECTOMY_KIDNEY_SIDES


class NephrectomyKidneyTypeListView(StringLookupListView):
    items = NEPHRECTOMY_KIDNEY_TYPES


class NephrectomyEntryTypeListView(StringLookupListView):
    items = NEPHRECTOMY_ENTRY_TYPES


def register_views(app):
    app.add_url_rule('/nephrectomies', view_func=NephrectomyListView.as_view('nephrectomy_list'))
    app.add_url_rule('/nephrectomies/<id>', view_func=NephrectomyDetailView.as_view('nephrectomy_detail'))
    app.add_url_rule('/nephrectomy-kidney-sides', view_func=NephrectomyKidneySideListView.as_view('nephrectomy_kidney_side_list'))
    app.add_url_rule('/nephrectomy-kidney-types', view_func=NephrectomyKidneyTypeListView.as_view('nephrectomy_kidney_type_list'))
    app.add_url_rule('/nephrectomy-entry-types', view_func=NephrectomyEntryTypeListView.as_view('nephrectomy_entry_type_list'))
