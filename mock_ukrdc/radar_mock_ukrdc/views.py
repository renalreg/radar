from radar.views.core import ApiView, request_json, response_json
from radar.serializers.ukrdc import SearchSerializer, ResultListSerializer
from radar_mock_ukrdc.validation import PatientSearchValidation


class PatientSearchView(ApiView):
    @request_json(SearchSerializer, PatientSearchValidation)
    @response_json(ResultListSerializer)
    def post(self, data):
        patient = {
            'name': {
                'given_name': data['name']['given_name'].upper(),
                'family_name': data['name']['family_name'].upper()
            },
            'birth_time': data['birth_time'],
            'gender': '1',
            'patient_numbers': [
                {
                    'number': '100000001',
                    'organization': {
                        'code': 'UKRDC',
                    },
                },
                {
                    'number': data['patient_number']['number'],
                    'organization': {
                        'code': data['patient_number']['organization']['code'],
                    },
                }
            ]
        }

        patients = [patient]

        return {'patients': patients}
