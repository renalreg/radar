from flask import Blueprint, abort, render_template
from flask_login import current_user

from radar.models.disease_groups import DiseaseGroup
from radar.models.patients import Patient
from radar.patients.views import get_patient_data


bp = Blueprint('diagnosis', __name__)


@bp.route('/<int:disease_group_id>')
def view_diagnosis(patient_id, disease_group_id):
    patient = Patient.query.get_or_404(patient_id)
    disease_group = DiseaseGroup.query.get_or_404(disease_group_id)

    if not patient.can_view(current_user):
        abort(403)

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        disease_group=disease_group,
    )

    return render_template('patient/diagnosis.html', **context)