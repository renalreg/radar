from radar.auth.sessions import current_user
from radar.views.core import ApiView, request_json, response_json, PermissionViewMixin
from radar_api.serializers.patients import PatientSerializer
from radar.recruit_patient import recruit_patient_search, recruit_patient
from radar.validation.recruit_patient import RecruitPatientValidation
from radar_api.serializers.recruit_patient import RecruitPatientSearchSerializer, \
    RecruitPatientResultListSerializer, RecruitPatientSerializer
from radar.permissions import RecruitPatientPermission


class RecruitPatientSearchView(PermissionViewMixin, ApiView):
    permission_classes = [RecruitPatientPermission]

    @request_json(RecruitPatientSearchSerializer)
    @response_json(RecruitPatientResultListSerializer)
    def post(self, data):
        results = recruit_patient_search(data)

        return {'results': results}


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
