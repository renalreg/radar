from cornflake.sqlalchemy_orm import ModelSerializer
from radar.api.serializers.nationalities import NationalitySerializer
from radar.api.serializers.patient_demographics import PatientDemographicsSerializer
from radar.api.views.common import (
    IntegerLookupListView,
    PatientObjectDetailView,
    PatientObjectListView,
    StringLookupListView,
    SystemObjectViewMixin,
)
from radar.api.views.generics import ListModelView
from radar.models.nationalities import Nationality
from radar.models.patient_codes import ETHNICITIES, GENDERS
from radar.models.patient_demographics import PatientDemographics


class PatientDemographicsListView(SystemObjectViewMixin, PatientObjectListView):
    serializer_class = PatientDemographicsSerializer
    model_class = PatientDemographics


class PatientDemographicsDetailView(SystemObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientDemographicsSerializer
    model_class = PatientDemographics


class EthnicityListView(StringLookupListView):
    items = ETHNICITIES


class GenderListView(IntegerLookupListView):
    items = GENDERS


class NationalityListView(ListModelView):
    serializer_class = NationalitySerializer
    model_class = Nationality


def register_views(app):
    app.add_url_rule('/patient-demographics', view_func=PatientDemographicsListView.as_view('patient_demographics_list'))
    app.add_url_rule('/patient-demographics/<id>', view_func=PatientDemographicsDetailView.as_view('patient_demographics_detail'))
    app.add_url_rule('/ethnicities', view_func=EthnicityListView.as_view('ethnicity_list'))
    app.add_url_rule('/genders', view_func=GenderListView.as_view('gender_list'))
    app.add_url_rule('/nationalities', view_func=NationalityListView.as_view('nationality_list'))
