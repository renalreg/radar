from flask import render_template, Blueprint
from flask.views import View
from radar.models import DiseaseGroup
from radar.patients.views import get_patient_detail_context


class DiagnosisDetailView(View):
    def dispatch_request(self, patient_id, disease_group_id):
        context = get_patient_detail_context(patient_id)

        # TODO
        context['disease_group'] = DiseaseGroup.query.get(disease_group_id)

        return render_template('patient/diagnosis.html', **context)

app = Blueprint('diagnoses', __name__)
app.add_url_rule('/<int:disease_group_id>/', view_func=DiagnosisDetailView.as_view('detail'))