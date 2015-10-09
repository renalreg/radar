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
