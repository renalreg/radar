from radar_api.serializers.patient_demographics import PatientDemographicsSerializer
from radar.auth.sessions import current_user
from radar.validation.patient_demographics import PatientDemographicsValidation
from radar.views.codes import CodedIntegerListView
from radar.models import PatientDemographics, GENDERS, ETHNICITIES
from radar.views.sources import RadarObjectViewMixin
from radar.views.patients import PatientObjectListView, PatientObjectDetailView
from radar.views.codes import CodedStringListView


class PatientDemographicsListView(RadarObjectViewMixin, PatientObjectListView):
    model_class = PatientDemographics
    validation_class = PatientDemographicsValidation

    def get_serializer(self):
        return PatientDemographicsSerializer(current_user)


class PatientDemographicsDetailView(RadarObjectViewMixin, PatientObjectDetailView):
    model_class = PatientDemographics
    validation_class = PatientDemographicsValidation

    def get_serializer(self):
        return PatientDemographicsSerializer(current_user)


class EthnicityListView(CodedStringListView):
    items = ETHNICITIES


class GenderListView(CodedIntegerListView):
    items = GENDERS


def register_views(app):
    app.add_url_rule('/patient-demographics', view_func=PatientDemographicsListView.as_view('patient_demographics_list'))
    app.add_url_rule('/patient-demographics/<id>', view_func=PatientDemographicsDetailView.as_view('patient_demographics_detail'))
    app.add_url_rule('/ethnicities', view_func=EthnicityListView.as_view('ethnicity_list'))
    app.add_url_rule('/genders', view_func=GenderListView.as_view('gender_list'))
