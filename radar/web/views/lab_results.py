from collections import defaultdict
from datetime import datetime

from flask import Blueprint, render_template, abort, request, jsonify, redirect, url_for
from flask_login import current_user
from sqlalchemy import desc, func

from radar.lib.database import db
from radar.web.forms.lab_results import LabResultTableForm, LabResultGraphForm, lab_order_to_form, \
    SelectLabOrderForm
from radar.lib.ordering import order_query, DESCENDING, ordering_from_request
from radar.lib.pagination import paginate_query
from radar.models.lab_results import LabOrderDefinition, LabOrder, LabResult
from radar.models.patients import Patient
from radar.web.views.patient_data import get_patient_data
from radar.lib.sda.models import SDABundle, SDALabOrder, SDALabResult
from radar.lib.utils import get_path_as_text, get_path_as_datetime


SORT_ITEM_PREFIX = 'item_'

LIST_ORDER_BY = {
    'date': SDALabOrder.from_time,
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
        .filter(SDABundle.patient == patient)

    query, ordering = order_query(query, LIST_ORDER_BY, 'date', DESCENDING)

    query = query.order_by(
        desc(SDALabOrder.from_time),
        SDALabOrder.data[('order_item', 'description')],
        SDALabResult.data[('test_item_code', 'description')],
    )

    pagination = paginate_query(query, default_per_page=50)
    sda_lab_results = pagination.items

    results = []

    for sda_lab_result in sda_lab_results:
        sda_lab_order = sda_lab_result.sda_lab_order

        result = dict()
        result['date'] = sda_lab_order.from_time
        result['test'] = get_path_as_text(sda_lab_order.data, ['order_item', 'description'])
        result['item'] = get_path_as_text(sda_lab_result.data, ['test_item_code', 'description'])
        result['value'] = get_path_as_text(sda_lab_result.data, ['result_value'])
        result['units'] = get_path_as_text(sda_lab_result.data, ['result_value_units'])
        result['source'] = get_path_as_text(sda_lab_order.data, ['entering_organization', 'description'])

        data_source = sda_lab_order.sda_bundle.data_source

        if data_source.can_edit(current_user):
            result['edit_url'] = data_source.edit_url()

        results.append(result)

    context = dict(
        results=results,
        patient=patient,
        patient_data=get_patient_data(patient),
        pagination=pagination,
        ordering=ordering,
    )

    return render_template('patient/lab_results_list.html', **context)


# TODO pagination
@bp.route('/table/')
def view_lab_result_table(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    form = LabResultTableForm(formdata=request.args, csrf_enabled=False)
    form.test_item.choices = get_test_item_choices()

    test_items = form.test_item.data

    if not test_items:
        test_items = ['creatinine']
        form.test_item.data = test_items

    # Sorting is done later to keep item grouping consistent
    sda_lab_results = SDALabResult.query\
        .join(SDALabResult.sda_lab_order)\
        .join(SDALabOrder.sda_bundle)\
        .filter(SDABundle.patient == patient)\
        .filter(SDALabResult.test_item_code.in_(test_items))\
        .order_by(SDALabOrder.id)\
        .order_by(SDALabResult.id)\
        .all()

    # Results list for display
    results = list()

    # Results for each group of fields
    result_dict = defaultdict(list)

    for sda_lab_result in sda_lab_results:
        sda_lab_order = sda_lab_result.sda_lab_order

        date = get_path_as_datetime(sda_lab_order.data, ['from_time'])
        source = get_path_as_text(sda_lab_order.data, ['entering_organization', 'description'])
        item = sda_lab_result.test_item_code
        value = get_path_as_text(sda_lab_result.data, ['result_value'])

        # Fields to group by
        group = (date, source)

        # Existing results in this group (i.e. result rows from a site at a particular time)
        group_results = result_dict[group]

        # The existing result to use
        result = None

        # Find an existing result to fill in before creating a new one
        for group_result in group_results:
            if item not in group_result['columns']:
                result = group_result
                break

        # First result for this group or all existing results have this item filled
        if result is None:
            result = dict()
            result['source'] = source
            result['date'] = date
            result['columns'] = dict()
            results.append(result)
            result_dict[group].append(result)

        result['columns'][item] = value

    sort_columns = ['date', 'source']
    sort_item_columns = [SORT_ITEM_PREFIX + x for x in test_items]
    sort_columns.extend(sort_item_columns)

    ordering = ordering_from_request(sort_columns, 'date', DESCENDING)

    sort_column = ordering.column
    sort_direction = ordering.direction

    def get_date(x):
        return x['date'] or datetime.min

    def get_source(x):
        return x['source']

    def get_item_value(x, item_column):
        value = x['columns'].get(item_column)

        if value is None:
            return None

        try:
            value = float(value)
        except ValueError:
            pass

        return value

    if sort_column.startswith(SORT_ITEM_PREFIX):
        sort_item_column = sort_column.split(SORT_ITEM_PREFIX)[1]
        sort_f = lambda x: (get_item_value(x, sort_item_column), get_date(x), get_source(x))
    elif sort_column == 'source':
        sort_f = lambda x: (get_source(x), get_date(x))
    else:
        sort_f = lambda x: (get_date(x), get_source(x))

    results = sorted(results, key=sort_f, reverse=(sort_direction == DESCENDING))

    # Convert columns from dict to list for display
    for result in results:
        result['columns'] = [result['columns'].get(x) for x in test_items]

    item_columns = zip([x.upper() for x in test_items], sort_item_columns)

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        results=results,
        item_columns=item_columns,
        ordering=ordering,
        form=form,
    )

    return render_template('patient/lab_results_table.html', **context)


@bp.route('/graph/')
def view_lab_result_graph(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    form = LabResultGraphForm()
    form.test_item.choices = get_test_item_choices()

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        form=form,
    )

    return render_template('patient/lab_results_graph.html', **context)


@bp.route('/graph/data.json')
def view_lab_result_graph_json(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    test_item = request.args.get('test_item')

    if test_item is None:
        abort(404)

    dt_column = SDALabOrder.from_time
    value_column = func.parse_numeric(SDALabResult.data['result_value'].astext)

    query = db.session\
        .query(dt_column, value_column)\
        .join(SDALabResult.sda_lab_order)\
        .join(SDALabOrder.sda_bundle)\
        .filter(
            SDABundle.patient == patient,
            SDALabResult.test_item_code == test_item.lower(),
            dt_column != None,
            value_column != None
        )\
        .order_by(dt_column)

    data = []

    for dt, value in query.all():
        data.append((dt.isoformat(), float(value)))

    return jsonify({
        'name': test_item.upper(),  # TODO
        'units': 'TODO',
        'data': data,
    })


@bp.route('/new/', endpoint='add_lab_result', methods=['GET', 'POST'])
@bp.route('/<int:record_id>/', endpoint='view_lab_result')
@bp.route('/<int:record_id>/', endpoint='edit_lab_result', methods=['GET', 'POST'])
def view_lab_result(patient_id, record_id=None):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    select_form = SelectLabOrderForm()
    select_form.lab_order_definition_id.choices = get_lab_order_choices()

    lab_order_definition = None
    form = None

    if record_id is None:
        lab_order = LabOrder(patient=patient)

        if select_form.validate_on_submit():
            lab_order_definition_id = select_form.lab_order_definition_id.data
            lab_order_definition = LabOrderDefinition.query.get_or_404(lab_order_definition_id)
            lab_order.lab_order_definition = lab_order_definition
    else:
        lab_order = LabOrder.query\
            .filter(LabOrder.patient == patient)\
            .filter(LabOrder.id == record_id)\
            .first_or_404()
        lab_order_definition = lab_order.lab_order_definition

    if lab_order_definition is not None:
        data = get_lab_order_form_data(lab_order)
        form_class = lab_order_to_form(lab_order_definition)
        form = form_class(obj=lab_order, data=data)

        if 'lab_order_form' in request.form and form.validate_on_submit():
            update_lab_order(lab_order, form)

            concept_map = lab_order.to_concepts()
            valid, errors = concept_map.validate()

            if valid:
                db.session.add(lab_order)
                db.session.commit()
                return redirect(url_for('lab_results.view_lab_result_list', patient_id=patient_id))
            else:
                form.add_errors(errors)

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        select_form=select_form,
        form=form,
        lab_order=lab_order,
        lab_order_definition=lab_order_definition,
    )

    return render_template('patient/lab_result.html', **context)


@bp.route('/forms/<int:lab_order_definition_id>/', methods=['GET', 'POST'])
def lab_result_form(patient_id, lab_order_definition_id):
    patient = Patient.query.get_or_404(patient_id)

    lab_order_definition = LabOrderDefinition.query.get_or_404(lab_order_definition_id)
    form_class = lab_order_to_form(lab_order_definition)
    lab_order = LabOrder(patient=patient)
    lab_order.lab_order_definition_id = lab_order_definition.id
    form = form_class(obj=lab_order)

    context = dict(
        form=form,
        lab_order_definition=lab_order_definition,
    )

    return render_template('patient/edit_lab_result.html', **context)


def get_test_item_choices():
    # TODO will get slow
    # TODO multiple labels for same code
    # TODO coding standards
    return db.session\
        .query(
            SDALabResult.test_item_code,
            SDALabResult.data[('test_item_code', 'description')]
        )\
        .order_by(SDALabResult.data[('test_item_code', 'description')])\
        .distinct()\
        .all()


def update_lab_order(lab_order, form):
    lab_order.unit = form.unit_id.obj
    lab_order.date = form.date.data
    lab_order.lab_results = []

    lab_result_definitions = lab_order.lab_order_definition.lab_result_definitions

    for lab_result_definition in lab_result_definitions:
        lab_result = LabResult()
        lab_result.lab_result_definition = lab_result_definition
        value = getattr(form, lab_result_definition.code).data
        lab_result.value = value
        lab_order.lab_results.append(lab_result)


def get_lab_order_form_data(lab_order):
    data = dict()

    for lab_result in lab_order.lab_results:
        data[lab_result.lab_result_definition.code] = lab_result.value

    return data


def get_lab_order_choices():
    choices = []

    lab_order_definitions = LabOrderDefinition.query\
        .order_by(LabOrderDefinition.description)\
        .all()

    for x in lab_order_definitions:
        choices.append((x.id, x.description))

    return choices