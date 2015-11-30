from radar.auth.sessions import current_user
from radar.views.core import ApiView, request_json, response_json, PermissionViewMixin
from radar_api.serializers.patients import PatientSerializer
from radar.recruit_patient import recruit_patient_search, recruit_patient
from radar.validation.recruit_patient import RecruitPatientValidation, RecruitPatientSearchValidation
from radar_api.serializers.recruit_patient import RecruitPatientSearchSerializer, \
    RecruitPatientResultListSerializer, RecruitPatientSerializer
from radar.permissions import RecruitPatientPermission
from radar.views.core import ListModelView
from radar_api.serializers.organisations import OrganisationSerializer
from radar.models.organisations import Organisation


class RecruitPatientSearchView(PermissionViewMixin, ApiView):
    permission_classes = [RecruitPatientPermission]

    @request_json(RecruitPatientSearchSerializer, RecruitPatientSearchValidation)
    @response_json(RecruitPatientResultListSerializer)
    def post(self, data):
        patients = recruit_patient_search(data)
        return {'patients': patients}


class RecruitPatientView(PermissionViewMixin, ApiView):
    permission_classes = [RecruitPatientPermission]

    @request_json(RecruitPatientSerializer, RecruitPatientValidation)
    @response_json(lambda: PatientSerializer(current_user))
    def post(self, data):
        patient = recruit_patient(data)
        return patient


def register_views(app):
    app.add_url_rule('/recruit-patient', view_func=RecruitPatientView.as_view('recruit_patient'))
    app.add_url_rule('/recruit-patient-search', view_func=RecruitPatientSearchView.as_view('recruit_patient_search'))
