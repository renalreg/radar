from flask import Blueprint, render_template, abort, request, jsonify, redirect, url_for
from flask_login import current_user
from sqlalchemy import desc

from radar.lib.lab_results import LabResultTable
from radar.models import Facility
from radar.web.forms.core import add_empty_choice
from radar.web.forms.lab_results import LabResultTableForm, LabResultGraphForm, \
    lab_group_to_form_data, lab_group_to_form, SelectLabGroupForm
from radar.lib.ordering import order_query, DESCENDING, ordering_from_request
from radar.lib.pagination import paginate_query
from radar.models.lab_results import LabResult, LabGroup, LabGroupDefinition, LabResultDefinition
from radar.models.patients import Patient
from radar.web.views.patient_data import get_patient_data, DetailService, PatientDataEditView, PatientDataAddView, \
    PatientDataDeleteView


RESULT_CODE_SORT_PREFIX = 'result_'

# TODO these should be functions
LIST_ORDER_BY = {
    'date': LabGroup.date,
    'group': LabGroupDefinition.name,
    'result': LabResultDefinition.name,
    'value': LabResult.value,
    'units': LabResultDefinition.units,
    'source': Facility.name,
}

bp = Blueprint('lab_results', __name__)


@bp.route('/')
def view_lab_result_list(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    query = LabResult.query\
        .join(LabResult.lab_group)\
        .join(LabResult.lab_result_definition)\
        .join(LabGroup.lab_group_definition)\
        .join(LabGroup.facility)\
        .filter(LabGroup.patient == patient)

    query, ordering = order_query(query, LIST_ORDER_BY, 'date', DESCENDING)

    query = query.order_by(
        desc(LabGroup.date),
        LabGroupDefinition.name,
        LabResultDefinition.name,
    )

    pagination = paginate_query(query, default_per_page=50)
    lab_results = pagination.items

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        pagination=pagination,
        ordering=ordering,
        lab_results=lab_results,
    )

    return render_template('patient/lab_results_list.html', **context)


# TODO pagination
@bp.route('/table/')
def view_lab_result_table(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    form = LabResultTableForm(formdata=request.args, csrf_enabled=False)
    form.result_codes.choices = get_result_code_choices()

    result_codes = form.result_codes.data

    # Default result codes
    if not result_codes:
        result_codes = ['CREATININE']

    lab_result_definitions = LabResultDefinition.query\
        .filter(LabResultDefinition.code.in_(result_codes))\
        .all()
    lab_result_definition_dict = {x.code: x for x in lab_result_definitions}

    # Remove invalid result codes
    result_codes = [x for x in result_codes if x in lab_result_definition_dict]
    form.result_codes.data = result_codes

    # Sorting is done later to keep item grouping consistent
    lab_results = LabResult.query\
        .join(LabResult.lab_result_definition)\
        .join(LabResult.lab_group)\
        .filter(LabResultDefinition.code.in_(result_codes))\
        .filter(LabGroup.patient == patient)\
        .order_by(LabGroup.id)\
        .order_by(LabResult.id)\
        .all()

    table = LabResultTable(result_codes)
    table.add_all(lab_results)

    # Build list of sortable columns
    sort_columns = ['date', 'source']
    sort_columns.extend([RESULT_CODE_SORT_PREFIX + x for x in result_codes])

    ordering = ordering_from_request(sort_columns, 'date', DESCENDING)

    sort_column = ordering.column
    reverse = ordering.direction == DESCENDING

    if sort_column.startswith(RESULT_CODE_SORT_PREFIX):
        sort_result_code = sort_column.split(RESULT_CODE_SORT_PREFIX)[1]
        table.sort_by_result_code(sort_result_code, reverse)
    elif sort_column == 'source':
        table.sort_by_facility(reverse)
    else:
        table.sort_by_date(reverse)

    result_columns = [(lab_result_definition_dict[x], RESULT_CODE_SORT_PREFIX + x) for x in result_codes]

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        table=table,
        ordering=ordering,
        form=form,
        result_columns=result_columns,
    )

    return render_template('patient/lab_results_table.html', **context)


@bp.route('/graph/')
def view_lab_result_graph(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    form = LabResultGraphForm()
    form.result_code.choices = get_result_code_choices()

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

    result_code = request.args.get('result_code')

    if result_code is None:
        abort(404)

    result_definition = LabResultDefinition.find_by_code(result_code)

    if result_definition is None:
        abort(404)

    lab_results = LabResult.query\
        .join(LabResult.lab_group)\
        .join(LabResult.lab_result_definition)\
        .filter(LabGroup.patient == patient)\
        .filter(LabResultDefinition.code == result_code)\
        .order_by(LabGroup.date, LabResult.id)\
        .all()

    data = []

    for lab_result in lab_results:
        data.append((lab_result.lab_group.date.isoformat(), float(lab_result.value)))

    return jsonify({
        'name': result_definition.name,
        'units': result_definition.units or '',
        'data': data,
    })


class LabGroupDetailService(DetailService):
    def get_object(self, patient, lab_group_id):
        lab_group = LabGroup.query\
            .filter(LabGroup.patient == patient)\
            .filter(LabGroup.id == lab_group_id)\
            .first()
        return lab_group

    def new_object(self, patient):
        return LabGroup(patient=patient)

    def get_form(self, obj, lab_group_definition=None):
        if obj.lab_group_definition is not None:
            lab_group_definition = obj.lab_group_definition

        form_class = lab_group_to_form(lab_group_definition)
        data = lab_group_to_form_data(obj)
        return form_class(obj=obj, data=data)


class LabGroupEditView(PatientDataEditView):
    def __init__(self):
        super(LabGroupEditView, self).__init__(
            LabGroupDetailService(current_user),
        )

    def saved(self, patient, obj):
        return redirect(url_for('lab_results.view_lab_result_list', patient_id=patient.id))

    def get_template_name(self):
        return 'patient/lab_group_form.html'


class LabGroupAddView(PatientDataAddView):
    def __init__(self):
        super(LabGroupAddView, self).__init__(
            LabGroupDetailService(current_user),
        )

        self.select_form = None

    def get_form(self, obj):
        select_form = SelectLabGroupForm()
        select_form.lab_group_definition_id.choices = get_lab_group_choices()
        self.select_form = select_form

        if select_form.validate_on_submit():
            lab_group_definition_id = select_form.lab_group_definition_id.data
            lab_group_definition = LabGroupDefinition.query.get_or_404(lab_group_definition_id)
            obj.lab_group_definition = lab_group_definition
            return super(LabGroupAddView, self).get_form(obj)
        else:
            return None

    def saved(self, patient, obj):
        return redirect(url_for('lab_results.view_lab_result_list', patient_id=patient.id))

    def get_template_name(self):
        return 'patient/lab_group_form.html'

    def get_context(self):
        return {
            'select_form': self.select_form
        }


class LabGroupDeleteView(PatientDataDeleteView):
    def __init__(self):
        super(LabGroupDeleteView, self).__init__(
            LabGroupDetailService(current_user),
        )

    def deleted(self, patient):
        return redirect(url_for('lab_results.view_lab_result_list', patient_id=patient.id))


bp.add_url_rule('/add/', view_func=LabGroupAddView.as_view('add_lab_group'))
bp.add_url_rule('/<int:lab_group_id>/edit/', view_func=LabGroupEditView.as_view('edit_lab_group'))
bp.add_url_rule('/<int:lab_group_id>/delete/', view_func=LabGroupDeleteView.as_view('delete_lab_group'))


@bp.route('/forms/<int:lab_group_definition_id>/', methods=['GET', 'POST'])
def lab_group_form(patient_id, lab_group_definition_id):
    patient = Patient.query.get_or_404(patient_id)

    lab_group_definition = LabGroupDefinition.query.get_or_404(lab_group_definition_id)
    form_class = lab_group_to_form(lab_group_definition)
    lab_group = LabGroup(patient=patient)
    lab_group.lab_group_definition_id = lab_group_definition.id
    form = form_class(obj=lab_group)

    context = dict(
        form=form,
        lab_group_definition=lab_group_definition,
    )

    return render_template('patient/lab_group_form_ajax.html', **context)


def get_result_code_choices():
    results = LabResultDefinition.query\
        .order_by(LabResultDefinition.name)\
        .all()

    return [(x.code, x.name) for x in results]


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


def get_lab_group_choices():
    choices = []

    lab_group_definitions = LabGroupDefinition.query\
        .order_by(LabGroupDefinition.name)\
        .all()

    for x in lab_group_definitions:
        choices.append((x.id, x.name))

    choices = add_empty_choice(choices)

    return choices