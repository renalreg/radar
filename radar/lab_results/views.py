from flask import Blueprint, render_template, abort
from flask_login import current_user

from radar.pagination import paginate_query
from radar.patients.models import Patient
from radar.patients.views import get_patient_data
from radar.sda.models import SDABundle, SDALabOrder, SDALabResult
from radar.utils import get_path_as_text, get_path_as_datetime


bp = Blueprint('lab_results', __name__)

@bp.route('/')
def view_lab_result_list(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    query = SDALabResult.query\
        .join(SDALabResult.sda_lab_order)\
        .join(SDALabOrder.sda_bundle)\
        .join(SDABundle.patient)\
        .filter(Patient.id == patient_id)

    pagination = paginate_query(query, default_per_page=50)
    sda_lab_results = pagination.items

    results = []

    for sda_lab_result in sda_lab_results:
        result = dict()
        result['date'] = get_path_as_datetime(sda_lab_result.sda_lab_order.data, ['from_time'])
        result['test'] = get_path_as_text(sda_lab_result.data, ['test_item_code', 'description'])
        result['value'] = get_path_as_text(sda_lab_result.data, ['result_value'])
        result['units'] = get_path_as_text(sda_lab_result.data, ['result_value_units'])
        results.append(result)

    context = dict(
        results=results,
        patient=patient,
        patient_data=get_patient_data(patient),
        pagination=pagination,
    )

    return render_template('patient/lab_results_list.html', **context)


@bp.route('/table/')
def view_lab_results_table(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
    )

    return render_template('patient/lab_results_table.html', **context)


@bp.route('/graph/')
def view_lab_results_graph(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
    )

    return render_template('patient/lab_results_graph.html', **context)