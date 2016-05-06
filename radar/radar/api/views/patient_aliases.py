from radar.models.patient_aliases import PatientAlias
from radar.api.serializers.patient_aliases import PatientAliasSerializer
from radar.api.views.common import (
    RadarObjectViewMixin,
    PatientObjectListView,
    PatientObjectDetailView,
    DemographicsViewMixin
)


class PatientAliasListView(RadarObjectViewMixin, DemographicsViewMixin, PatientObjectListView):
    serializer_class = PatientAliasSerializer
    model_class = PatientAlias


class PatientAliasDetailView(RadarObjectViewMixin, DemographicsViewMixin, PatientObjectDetailView):
    serializer_class = PatientAliasSerializer
    model_class = PatientAlias


def register_views(app):
    app.add_url_rule('/patient-aliases', view_func=PatientAliasListView.as_view('patient_alias_list'))
    app.add_url_rule('/patient-aliases/<id>', view_func=PatientAliasDetailView.as_view('patient_alias_detail'))
