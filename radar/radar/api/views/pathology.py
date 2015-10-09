from radar.api.serializers.pathology import PathologySerializer
from radar.lib.models import PATHOLOGY_KIDNEY_TYPES, PATHOLOGY_KIDNEY_SIDES, Pathology
from radar.lib.validation.pathology_validation import PathologyValidation
from radar.lib.views.codes import CodedStringListView
from radar.lib.views.data_sources import DataSourceObjectViewMixin
from radar.lib.views.patients import PatientObjectDetailView, PatientObjectListView


class PathologyListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = PathologySerializer
    model_class = Pathology
    validation_class = PathologyValidation


class PathologyDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = PathologySerializer
    model_class = Pathology
    validation_class = PathologyValidation


class PathologyKidneyTypeListView(CodedStringListView):
    items = PATHOLOGY_KIDNEY_TYPES


class PathologyKidneySideListView(CodedStringListView):
    items = PATHOLOGY_KIDNEY_SIDES
