from radar.api.serializers.hospitalisations import HospitalisationSerializer
from radar.api.views.common import (
    SourceObjectViewMixin,
    PatientObjectDetailView,
    PatientObjectListView
)
from radar.models.hospitalisations import Hospitalisation


class HospitalisationListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = HospitalisationSerializer
    model_class = Hospitalisation


class HospitalisationDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = HospitalisationSerializer
    model_class = Hospitalisation


def register_views(app):
    app.add_url_rule('/hospitalisations', view_func=HospitalisationListView.as_view('hospitalisation_list'))
    app.add_url_rule('/hospitalisations/<id>', view_func=HospitalisationDetailView.as_view('hospitalisation_detail'))
