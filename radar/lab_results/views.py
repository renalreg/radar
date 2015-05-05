from collections import defaultdict

from flask import Blueprint, render_template, abort
from flask_login import current_user
from sqlalchemy import desc, func
from radar.database import db

from radar.ordering import order_query, DESCENDING, ordering_from_request
from radar.pagination import paginate_query
from radar.patients.models import Patient
from radar.patients.views import get_patient_data
from radar.sda.models import SDABundle, SDALabOrder, SDALabResult
from radar.utils import get_path_as_text, get_path_as_datetime


LIST_ORDER_BY = {
    'date': SDALabOrder.data['from_time'],
    'test': SDALabOrder.data[('order_item', 'description')],
    'item': SDALabResult.data[('test_item_code', 'description')],
    'value': [func.parse_numeric(SDALabResult.data['result_value'].astext), SDALabResult.data['result_value']],
    'units': SDALabResult.data['result_value_units'],
    'source': SDALabOrder.data[('entering_organization', 'description')],
}

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

    query, ordering = order_query(query, LIST_ORDER_BY, 'date', DESCENDING)

    query = query.order_by(
        desc(SDALabOrder.data['from_time']),
        SDALabOrder.data[('order_item', 'description')],
        SDALabResult.data[('test_item_code', 'description')],
    )

    pagination = paginate_query(query, default_per_page=50)
    sda_lab_results = pagination.items

    results = []

    for sda_lab_result in sda_lab_results:
        sda_lab_order = sda_lab_result.sda_lab_order

        result = dict()
        result['date'] = get_path_as_datetime(sda_lab_order.data, ['from_time'])
        result['test'] = get_path_as_text(sda_lab_order.data, ['order_item', 'description'])
        result['item'] = get_path_as_text(sda_lab_result.data, ['test_item_code', 'description'])
        result['value'] = get_path_as_text(sda_lab_result.data, ['result_value'])
        result['units'] = get_path_as_text(sda_lab_result.data, ['result_value_units'])
        result['source'] = get_path_as_text(sda_lab_order.data, ['entering_organization', 'description'])
        results.append(result)

    context = dict(
        results=results,
        patient=patient,
        patient_data=get_patient_data(patient),
        pagination=pagination,
        ordering=ordering,
    )

    return render_template('patient/lab_results_list.html', **context)


@bp.route('/table/')
def view_lab_result_table(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    columns = ['INR', 'HB', 'WBC']

    sda_lab_results = SDALabResult.query\
        .join(SDALabResult.sda_lab_order)\
        .join(SDALabOrder.sda_bundle)\
        .join(SDABundle.patient)\
        .filter(Patient.id == patient_id)\
        .filter(func.upper(SDALabResult.data[('test_item_code', 'code')].astext).in_(columns))\
        .order_by(SDALabResult.id)\
        .all()

    results = list()
    result_dict = defaultdict(list)

    for sda_lab_result in sda_lab_results:
        sda_lab_order = sda_lab_result.sda_lab_order

        date = get_path_as_datetime(sda_lab_order.data, ['from_time'])
        source = get_path_as_text(sda_lab_order.data, ['entering_organization', 'description'])
        item = get_path_as_text(sda_lab_result.data, ['test_item_code', 'description']).upper()
        value = get_path_as_text(sda_lab_result.data, ['result_value'])

        group = (date, source)
        group_results = result_dict[group]

        result = None

        for group_result in group_results:
            print group_result

            if item not in group_result['columns']:
                result = group_result
                break

        if result is None:
            result = dict()
            result['source'] = source
            result['date'] = date
            result['columns'] = dict()
            results.append(result)
            result_dict[group].append(result)
        else:
            result = results[-1]

        result['columns'][item] = value

    for result in results:
        result['columns'] = [result['columns'].get(x) for x in columns]

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        results=results,
        columns=columns
    )

    return render_template('patient/lab_results_table.html', **context)


@bp.route('/graph/')
def view_lab_result_graph(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
    )

    return render_template('patient/lab_results_graph.html', **context)