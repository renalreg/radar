from radar.views.core import ApiView, request_json, response_json
from radar_mock_ukrdc.serializers import PatientSearchSerializer, PatientResultListSerializer
from radar_mock_ukrdc.validation import PatientSearchValidation


class PatientSearchView(ApiView):
    @request_json(PatientSearchSerializer, PatientSearchValidation)
    @response_json(PatientResultListSerializer)
    def post(self, data):
        patient = {
            'name': {
                'given': data['name']['given'].capitalize(),
                'family': data['name']['family'].capitalize()
            },
            'birth_time': data['birth_time'],
            'gender': '1',
            'patient_numbers': [
                {
                    'number': '1000000001',
                    'code_system': 'ukrdc',
                },
                {
                    'number': data['patient_number']['number'],
                    'code_system': data['patient_number']['code_system'],
                }
            ]
        }

        patients = [patient]

        return {'patients': patients}
