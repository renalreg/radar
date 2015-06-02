from flask import Blueprint, render_template

from radar.models.patients import Patient
from radar.web.views.patient_data import get_patient_data


bp = Blueprint('pathology', __name__)


@bp.route('/')
def view_pathology_list(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
    )

    return render_template('patient/pathology.html', **context)
