from radar.api.serializers.patient_demographics import PatientDemographicsSerializer, EthnicityCodeSerializer
from radar.lib.auth import current_user
from radar.lib.patient_demographics import PatientDemographicsProxy
from radar.lib.validation.patient_demographics import PatientDemographicsValidation
from radar.lib.views.codes import CodedIntegerListView
from radar.lib.views.core import ListModelView
from radar.lib.models import PatientDemographics, EthnicityCode, GENDERS
from radar.lib.views.data_sources import RadarObjectViewMixin
from radar.lib.views.patients import PatientObjectListView, PatientObjectDetailView


class PatientDemographicsListView(RadarObjectViewMixin, PatientObjectListView):
    serializer_class = PatientDemographicsSerializer
    model_class = PatientDemographics
    validation_class = PatientDemographicsValidation

    def get_object_list(self):
        demographics_list, pagination = super(PatientDemographicsListView, self).get_object_list()

        # Wrap demographics in proxy object
        demographics_list = [PatientDemographicsProxy(x, current_user) for x in demographics_list]

        return demographics_list, pagination


class PatientDemographicsDetailView(RadarObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientDemographicsSerializer
    model_class = PatientDemographics
    validation_class = PatientDemographicsValidation

    def get_object(self):
        demographics = super(PatientDemographicsDetailView, self).get_object()
        return PatientDemographicsProxy(demographics, current_user)


class EthnicityCodeListView(ListModelView):
    serializer_class = EthnicityCodeSerializer
    model_class = EthnicityCode


class GenderListView(CodedIntegerListView):
    items = GENDERS
