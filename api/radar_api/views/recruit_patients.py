from radar.auth.sessions import current_user

from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, IntegerField, DateField, ListField
from radar.views.core import ApiView, request_json, response_json
from radar_api.serializers.patients import PatientSerializer
from radar.models.patients import Patient


class RecruitPatientSearchSerializer(Serializer):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    nhs_no = StringField()
    chi_no = StringField()


class RecruitPatientResultSerializer(Serializer):
    mpiid = IntegerField()
    radar_id = IntegerField()
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    nhs_no = StringField()
    chi_no = StringField()


class RecruitPatientResultListSerializer(Serializer):
    results = ListField(RecruitPatientResultSerializer())


class RecruitPatientSerializer(Serializer):
    mpiid = IntegerField()
    radar_id = IntegerField()
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    nhs_no = StringField()
    chi_no = StringField()


class RecruitPatientSearchView(ApiView):
    @request_json(RecruitPatientSearchSerializer)
    @response_json(RecruitPatientResultListSerializer)
    def post(self, data):
        # TODO
        result = {
            'mpiid': 1,
            'first_name': data['first_name'].capitalize(),
            'last_name': data['last_name'].capitalize(),
            'date_of_birth': data['date_of_birth']
        }

        results = [result]

        return {'results': results}


class RecruitPatientView(ApiView):
    @request_json(RecruitPatientSerializer)
    @response_json(lambda: PatientSerializer(current_user))
    def post(self, data):
        # TODO
        return Patient.query.get(1)


def register_views(app):
    app.add_url_rule('/recruit-patient', view_func=RecruitPatientView.as_view('recruit_patient'))
    app.add_url_rule('/recruit-patient-search', view_func=RecruitPatientSearchView.as_view('recruit_patient_search'))
