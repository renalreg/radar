from radar.api.serializers.patient_numbers import PatientNumberSerializer
from radar.lib.views import PatientDataList, FacilityDataMixin, PatientDataDetail
from radar.models import PatientNumber


class PatientNumberList(FacilityDataMixin, PatientDataList):
    serializer_class = PatientNumberSerializer
    model_class = PatientNumber


class PatientNumberDetail(FacilityDataMixin, PatientDataDetail):
    serializer_class = PatientNumberSerializer
    model_class = PatientNumber
