from radar.api.serializers.patient_addresses import PatientAddressSerializer
from radar.lib.views import PatientDataList, FacilityDataMixin, PatientDataDetail
from radar.models import PatientAddress


class PatientAddressList(FacilityDataMixin, PatientDataList):
    serializer_class = PatientAddressSerializer
    model_class = PatientAddress


class PatientAddressDetail(FacilityDataMixin, PatientDataDetail):
    serializer_class = PatientAddressSerializer
    model_class = PatientAddress
