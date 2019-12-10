from radar.api.serializers.patient_demographics import PatientDemographicsSerializer
from radar.api.views.common import (
    IntegerLookupListView,
    PatientObjectDetailView,
    PatientObjectListView,
    SystemObjectViewMixin,
)
from radar.models.patient_codes import GENDERS, SIGNED_OFF
from radar.models.patient_demographics import PatientDemographics


class PatientDemographicsListView(SystemObjectViewMixin, PatientObjectListView):
    serializer_class = PatientDemographicsSerializer
    model_class = PatientDemographics


class PatientDemographicsDetailView(SystemObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientDemographicsSerializer
    model_class = PatientDemographics


class GenderListView(IntegerLookupListView):
    items = GENDERS

class SignedOffListView(IntegerLookupListView):
    items = SIGNED_OFF


def register_views(app):
    app.add_url_rule(
        '/patient-demographics',
        view_func=PatientDemographicsListView.as_view('patient_demographics_list')
    )
    app.add_url_rule(
        '/patient-demographics/<id>',
        view_func=PatientDemographicsDetailView.as_view('patient_demographics_detail')
    )
    app.add_url_rule('/genders', view_func=GenderListView.as_view('gender_list'))
    app.add_url_rule('/signedOffStates', view_func=SignedOffListView.as_view('signed_off_list'))
