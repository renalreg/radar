from radar.auth.sessions import current_user
from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, IntegerField, DateField, ListField
from radar.views.core import ApiView, request_json, response_json
from radar_api.serializers.patients import PatientSerializer
from radar.recruit_patient import recruit_patient_search, recruit_patient
from radar_api.serializers.patient_demographics import EthnicityCodeReferenceField
from radar_api.serializers.cohorts import CohortReferenceField
from radar_api.serializers.organisations import OrganisationReferenceField
from radar.serializers.codes import CodedIntegerSerializer
from radar.models.patients import GENDERS
from radar.validation.recruit_patient import RecruitPatientValidation


class RecruitPatientSearchSerializer(Serializer):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    patient_number = StringField()


class RecruitPatientResultSerializer(Serializer):
    mpiid = IntegerField()
    radar_id = IntegerField()
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    gender = CodedIntegerSerializer(GENDERS)
    nhs_no = StringField()
    chi_no = StringField()


class RecruitPatientResultListSerializer(Serializer):
    results = ListField(RecruitPatientResultSerializer())


class RecruitPatientSerializer(Serializer):
    mpiid = IntegerField()
    radar_id = IntegerField()
    recruited_by_organisation = OrganisationReferenceField()
    cohort = CohortReferenceField()
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    gender = CodedIntegerSerializer(GENDERS)
    ethnicity = EthnicityCodeReferenceField()
    nhs_no = StringField()
    chi_no = StringField()


class RecruitPatientSearchView(ApiView):
    @request_json(RecruitPatientSearchSerializer)
    @response_json(RecruitPatientResultListSerializer)
    def post(self, data):
        results = recruit_patient_search(data)

        return {'results': results}


class RecruitPatientView(ApiView):
    @request_json(RecruitPatientSerializer, RecruitPatientValidation)
    @response_json(lambda: PatientSerializer(current_user))
    def post(self, data):
        patient = recruit_patient(data)
        return patient


def register_views(app):
    app.add_url_rule('/recruit-patient', view_func=RecruitPatientView.as_view('recruit_patient'))
    app.add_url_rule('/recruit-patient-search', view_func=RecruitPatientSearchView.as_view('recruit_patient_search'))
