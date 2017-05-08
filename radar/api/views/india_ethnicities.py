from radar.api.serializers.india_ethnicities import IndiaEthnicitySerializer
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView,
    SystemObjectViewMixin,
)
from radar.models.india_ethnicities import IndiaEthnicity


class IndiaEthnicityListView(SystemObjectViewMixin, PatientObjectListView):
    serializer_class = IndiaEthnicitySerializer
    model_class = IndiaEthnicity


class IndiaEthnicityDetailView(SystemObjectViewMixin, PatientObjectDetailView):
    serializer_class = IndiaEthnicitySerializer
    model_class = IndiaEthnicity


def register_views(app):
    app.add_url_rule('/india-ethnicities', view_func=IndiaEthnicityListView.as_view('india_ethnicity_list'))
    app.add_url_rule('/india-ethnicities/<id>', view_func=IndiaEthnicityDetailView.as_view('india_ethnicity_detail'))
