from radar_api.serializers.transplants import TransplantSerializer
from radar.models import TRANSPLANT_TYPES, Transplant
from radar.validation.transplants import TransplantValidation
from radar.views.codes import CodedStringListView
from radar.views.data_sources import DataSourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class TransplantListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = TransplantSerializer
    model_class = Transplant
    validation_class = TransplantValidation


class TransplantDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = TransplantSerializer
    model_class = Transplant
    validation_class = TransplantValidation


class TransplantTypeListView(CodedStringListView):
    items = TRANSPLANT_TYPES


def register_views(app):
    app.add_url_rule('/transplants', view_func=TransplantListView.as_view('transplant_list'))
    app.add_url_rule('/transplants/<int:id>', view_func=TransplantDetailView.as_view('transplant_detail'))
    app.add_url_rule('/transplant-types', view_func=TransplantTypeListView.as_view('transplant_type_list'))
