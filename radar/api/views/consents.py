from flask import jsonify, request

from radar.api.serializers.consents import (
    ConsentSerializer,
    PatientConsentSerializer,
)

from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView,
)

from radar.api.views.generics import ListModelView

from radar.database import db
from radar.exceptions import BadRequest
from radar.models.consents import Consent, PatientConsent
from radar.utils import camel_case_keys


class ConsentListView(ListModelView):
    serializer_class = ConsentSerializer
    model_class = Consent


class PatientConsentListView(PatientObjectListView):
    serializer_class = PatientConsentSerializer
    model_class = PatientConsent

    def create(self):
        json = request.get_json()
        print(json)
        if json is None:
            raise BadRequest()
        # consents = [consent_id for consent_id, selected in json.get('consents', {}).items() if selected]

        # json['consents'] = consents
        serializer = self.get_serializer(data=json)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        db.session.add(obj)
        db.session.commit()

        data = serializer.data
        data = camel_case_keys(data)

        return jsonify(data), 200


class PatientConsentDetailView(PatientObjectDetailView):
    serializer_class = PatientConsentSerializer
    model_class = PatientConsent


def register_views(app):
    app.add_url_rule('/patient-consents', view_func=PatientConsentListView.as_view('patient_consent_list'))
    app.add_url_rule('/patient-consents/<id>', view_func=PatientConsentDetailView.as_view('patient_consent_detail'))
    app.add_url_rule('/consents', view_func=ConsentListView.as_view('consent_list'))
    # app.add_url_rule('/consents/<id>', view_func=ConsentDetailView.as_view('consent_detail'))
