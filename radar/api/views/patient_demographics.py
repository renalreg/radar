from radar.api.serializers.patient_demographics import PatientDemographicsSerializer, EthnicityCodeSerializer
from radar.lib.validation.patient_demographics import PatientDemographicsValidation
from radar.lib.views.core import ListModelView
from radar.lib.models import PatientDemographics, EthnicityCode
from radar.lib.views.data_sources import DataSourceObjectViewMixin
from radar.lib.views.patients import PatientObjectListView, PatientObjectDetailView


class PatientDemographicsListView(DataSourceObjectViewMixin, PatientObjectListView):
    serializer_class = PatientDemographicsSerializer
    model_class = PatientDemographics
    validation_class = PatientDemographicsValidation


class PatientDemographicsDetailView(DataSourceObjectViewMixin, PatientObjectDetailView):
    serializer_class = PatientDemographicsSerializer
    model_class = PatientDemographics
    validation_class = PatientDemographicsValidation


class EthnicityCodeListView(ListModelView):
    serializer_class = EthnicityCodeSerializer
    model_class = EthnicityCode
