from radar_api.serializers.nephrectomies import NephrectomySerializer
from radar.models.nephrectomies import Nephrectomy, NEPHRECTOMY_KIDNEY_SIDES, NEPHRECTOMY_KIDNEY_TYPES, NEPHRECTOMY_ENTRY_TYPES
from radar.validation.nephrectomies import NephrectomyValidation
from radar.views.codes import CodedStringListView
from radar.views.data_sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class NephrectomyListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = NephrectomySerializer
    model_class = Nephrectomy
    validation_class = NephrectomyValidation


class NephrectomyDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = NephrectomySerializer
    model_class = Nephrectomy
    validation_class = NephrectomyValidation


class NephrectomyKidneySideListView(CodedStringListView):
    items = NEPHRECTOMY_KIDNEY_SIDES


class NephrectomyKidneyTypeListView(CodedStringListView):
    items = NEPHRECTOMY_KIDNEY_TYPES


class NephrectomyEntryTypeListView(CodedStringListView):
    items = NEPHRECTOMY_ENTRY_TYPES


def register_views(app):
    app.add_url_rule('/nephrectomies', view_func=NephrectomyListView.as_view('nephrectomy_list'))
    app.add_url_rule('/nephrectomies/<int:id>', view_func=NephrectomyDetailView.as_view('nephrectomy_detail'))
    app.add_url_rule('/nephrectomy-kidney-sides', view_func=NephrectomyKidneySideListView.as_view('nephrectomy_kidney_side_list'))
    app.add_url_rule('/nephrectomy-kidney-types', view_func=NephrectomyKidneyTypeListView.as_view('nephrectomy_kidney_type_list'))
    app.add_url_rule('/nephrectomy-entry-types', view_func=NephrectomyEntryTypeListView.as_view('nephrectomy_entry_type_list'))
