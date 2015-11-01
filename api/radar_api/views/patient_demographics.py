from radar_api.serializers.patient_demographics import PatientDemographicsSerializer, EthnicityCodeSerializer
from radar.auth.sessions import current_user
from radar.validation.patient_demographics import PatientDemographicsValidation
from radar.views.codes import CodedIntegerListView
from radar.views.core import ListModelView
from radar.models import PatientDemographics, EthnicityCode, GENDERS
from radar.views.data_sources import RadarObjectViewMixin
from radar.views.patients import PatientObjectListView, PatientObjectDetailView


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


class EthnicityCodeListView(ListModelView):
    serializer_class = EthnicityCodeSerializer
    model_class = EthnicityCode


class GenderListView(CodedIntegerListView):
    items = GENDERS


def register_views(app):
    app.add_url_rule('/patient-demographics', view_func=PatientDemographicsListView.as_view('patient_demographics_list'))
    app.add_url_rule('/patient-demographics/<id>', view_func=PatientDemographicsDetailView.as_view('patient_demographics_detail'))
    app.add_url_rule('/ethnicity-codes', view_func=EthnicityCodeListView.as_view('ethnicity_code_list'))
    app.add_url_rule('/genders', view_func=GenderListView.as_view('gender_list'))
