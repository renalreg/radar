from radar.models.patient_demographics import PatientDemographics
from radar.models.patients import GENDERS, ETHNICITIES
from radar.serializers.patient_demographics import PatientDemographicsSerializer
from radar.views.common import (
    PatientObjectListView,
    PatientObjectDetailView,
    RadarObjectViewMixin,
    StringLookupListView,
    IntegerLookupListView
)


class PatientDemographicsListView(RadarObjectViewMixin, PatientObjectListView):
    serializer_class = PatientDemographicsSerializer
    model_class = PatientDemographics


class PatientDemographicsDetailView(RadarObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientDemographicsSerializer
    model_class = PatientDemographics


class EthnicityListView(StringLookupListView):
    items = ETHNICITIES


class GenderListView(IntegerLookupListView):
    items = GENDERS


def register_views(app):
    app.add_url_rule('/patient-demographics', view_func=PatientDemographicsListView.as_view('patient_demographics_list'))
    app.add_url_rule('/patient-demographics/<id>', view_func=PatientDemographicsDetailView.as_view('patient_demographics_detail'))
    app.add_url_rule('/ethnicities', view_func=EthnicityListView.as_view('ethnicity_list'))
    app.add_url_rule('/genders', view_func=GenderListView.as_view('gender_list'))
