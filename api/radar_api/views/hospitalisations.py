from radar_api.serializers.hospitalisations import HospitalisationSerializer
from radar.models import Hospitalisation
from radar.validation.hospitalisations import HospitalisationValidation
from radar.views.sources import SourceObjectViewMixin
from radar.views.patients import PatientObjectDetailView, PatientObjectListView


class HospitalisationListView(SourceObjectViewMixin, PatientObjectListView):
    serializer_class = HospitalisationSerializer
    model_class = Hospitalisation
    validation_class = HospitalisationValidation


class HospitalisationDetailView(SourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = HospitalisationSerializer
    model_class = Hospitalisation
    validation_class = HospitalisationValidation


def register_views(app):
    app.add_url_rule('/hospitalisations', view_func=HospitalisationListView.as_view('hospitalisation_list'))
    app.add_url_rule('/hospitalisations/<id>', view_func=HospitalisationDetailView.as_view('hospitalisation_detail'))
