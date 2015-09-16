from radar.api.serializers.patient_demographics import PatientDemographicsSerializer, EthnicityCodeSerializer
from radar.lib.validation.patient_demographics import PatientDemographicsValidation
from radar.lib.views.core import ListModelView, CodedIntegerListView
from radar.lib.models import PatientDemographics, EthnicityCode, GENDERS
from radar.lib.views.data_sources import RadarObjectViewMixin
from radar.lib.views.patients import PatientObjectListView, PatientObjectDetailView


class PatientDemographicsListView(RadarObjectViewMixin, PatientObjectListView):
    serializer_class = PatientDemographicsSerializer
    model_class = PatientDemographics
    validation_class = PatientDemographicsValidation


class PatientDemographicsDetailView(RadarObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientDemographicsSerializer
    model_class = PatientDemographics
    validation_class = PatientDemographicsValidation


class EthnicityCodeListView(ListModelView):
    serializer_class = EthnicityCodeSerializer
    model_class = EthnicityCode


class GenderListView(CodedIntegerListView):
    items = GENDERS
