from flask import Blueprint, abort, render_template
from flask_login import current_user
from radar.patients.models import Patient
from radar.patients.views import get_patient_data

bp = Blueprint('renal_imaging', __name__)


@bp.route('/')
def view_renal_imaging_list(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
    )

    return render_template('patient/renal_imaging_list.html', **context)


@bp.route('/new/', endpoint='add_renal_imaging', methods=['GET', 'POST'])
@bp.route('/<int:renal_imaging_id>/', endpoint='view_renal_imaging')
@bp.route('/<int:renal_imaging_id>/', endpoint='edit_renal_imaging', methods=['GET', 'POST'])
def view_renal_imaging(patient_id, renal_imaging_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
    )

    return render_template('patient/renal_imaging.html', **context)