from radar.views.core import ApiView, request_json, response_json
from radar_mock_ukrdc.serializers import PatientSearchSerializer, PatientResultListSerializer
from radar_mock_ukrdc.validation import PatientSearchValidation


class PatientSearchView(ApiView):
    @request_json(PatientSearchSerializer, PatientSearchValidation)
    @response_json(PatientResultListSerializer)
    def post(self, data):
        result = {
            'first_name': data['first_name'].capitalize(),
            'last_name': data['last_name'].capitalize(),
            'date_of_birth': data['date_of_birth']
        }

        results = [result]

        return {'results': results}
