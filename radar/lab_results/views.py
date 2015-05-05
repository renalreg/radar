from flask import Blueprint, render_template, abort, request, url_for, redirect
from flask_login import current_user

from radar.concepts.core import validate_concepts, concepts_to_sda_bundle
from radar.concepts.utils import add_errors_to_form
from radar.database import db
from radar.medications.forms import MedicationForm
from radar.medications.models import Medication
from radar.patients.models import Patient
from radar.patients.views import get_patient_data
from radar.sda.models import SDAMedication, SDABundle, SDALabOrder, SDALabResult
from radar.utils import get_path_as_text, get_path_as_datetime


bp = Blueprint('lab_results', __name__)

@bp.route('/')
def view_lab_result_list(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    sda_lab_results = SDALabResult.query\
        .join(SDALabResult.sda_lab_order)\
        .join(SDALabOrder.sda_bundle)\
        .join(SDABundle.patient)\
        .filter(Patient.id == patient_id)\
        .all()

    results = []

    for sda_lab_result in sda_lab_results:
        result = dict()
        result['code'] = get_path_as_text(sda_lab_result.data, ['test_item_code', 'code'])
        result['value'] = get_path_as_text(sda_lab_result.data, ['result_value'])
        results.append(result)

    context = dict(
        results=results,
        patient=patient,
        patient_data=get_patient_data(patient)
    )

    return render_template('patient/lab_results.html', **context)