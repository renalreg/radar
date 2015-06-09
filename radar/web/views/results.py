from flask import Blueprint, render_template, abort, request, jsonify, redirect, url_for
from flask_login import current_user
from sqlalchemy import desc
from radar.lib.results import ResultTable

from radar.models import Facility, ResultGroupDefinition, ResultDefinition, ResultGroup, Result
from radar.web.forms.core import add_empty_choice
from radar.web.forms.results import SelectResultGroupForm, ResultTableForm, ResultGraphForm, result_group_to_form, \
    result_group_to_form_data, SelectAddResultGroupForm
from radar.lib.ordering import order_query, DESCENDING, ordering_from_request
from radar.lib.pagination import paginate_query
from radar.models.patients import Patient
from radar.web.views.patient_data import get_patient_data, PatientDataDetailService, PatientDataEditView, PatientDataAddView, \
    PatientDataDeleteView, PatientDataDetailView


RESULT_CODE_SORT_PREFIX = 'result_'

# TODO these should be functions
LIST_ORDER_BY = {
    'date': ResultGroup.date,
    'group': ResultGroupDefinition.name,
    'result': ResultDefinition.name,
    'value': Result.value,
    'units': ResultDefinition.units,
    'source': Facility.name,
}

bp = Blueprint('results', __name__)


@bp.route('/')
def view_result_list(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
    )

    form = SelectResultGroupForm(formdata=request.args, csrf_enabled=False)
    result_group_choices = get_result_group_choices()
    result_group_choices.insert(0, ('', 'All'))
    form.result_group_definition_id.choices = result_group_choices

    if form.validate():
        result_group_definition_id = form.result_group_definition_id.data
    else:
        result_group_definition_id = None

    query = Result.query\
        .join(Result.result_group)\
        .join(Result.result_definition)\
        .join(ResultGroup.result_group_definition)\
        .join(ResultGroup.facility)\
        .filter(ResultGroup.patient == patient)

    if result_group_definition_id is not None:
        result_group_definition = ResultGroupDefinition.query.get_or_404(result_group_definition_id)
        query = query.filter(ResultGroup.result_group_definition == result_group_definition)
        context['result_group_definition'] = result_group_definition

    query, ordering = order_query(query, LIST_ORDER_BY, 'date', DESCENDING)

    query = query.order_by(
        desc(ResultGroup.date),
        ResultGroupDefinition.name,
        ResultDefinition.name,
    )

    pagination = paginate_query(query, default_per_page=50)
    results = pagination.items

    context.update(dict(
        pagination=pagination,
        ordering=ordering,
        results=results,
        form=form,
    ))

    return render_template('patient/results_list.html', **context)


# TODO pagination
@bp.route('/table/')
def view_result_table(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    form = ResultTableForm(formdata=request.args, csrf_enabled=False)
    form.result_codes.choices = get_result_code_choices()

    result_codes = form.result_codes.data

    # Default result codes
    if not result_codes:
        result_codes = ['CREATININE']

    result_definitions = ResultDefinition.query\
        .filter(ResultDefinition.code.in_(result_codes))\
        .all()
    result_definition_dict = {x.code: x for x in result_definitions}

    # Remove invalid result codes
    result_codes = [x for x in result_codes if x in result_definition_dict]
    form.result_codes.data = result_codes

    if result_codes:
        # Sorting is done later to keep item grouping consistent
        results = Result.query\
            .join(Result.result_definition)\
            .join(Result.result_group)\
            .filter(ResultDefinition.code.in_(result_codes))\
            .filter(ResultGroup.patient == patient)\
            .order_by(ResultGroup.id)\
            .order_by(Result.id)\
            .all()
    else:
        results = []

    table = ResultTable(result_codes)
    table.add_all(results)

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

    result_columns = [(result_definition_dict[x], RESULT_CODE_SORT_PREFIX + x) for x in result_codes]

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        table=table,
        ordering=ordering,
        form=form,
        result_columns=result_columns,
    )

    return render_template('patient/results_table.html', **context)


@bp.route('/graph/')
def view_result_graph(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    form = ResultGraphForm()
    form.result_code.choices = get_result_code_choices()

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        form=form,
    )

    return render_template('patient/results_graph.html', **context)


@bp.route('/graph/data.json')
def view_result_graph_json(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    result_code = request.args.get('result_code')

    if result_code is None:
        abort(404)

    result_definition = ResultDefinition.find_by_code(result_code)

    if result_definition is None:
        abort(404)

    results = Result.query\
        .join(Result.result_group)\
        .join(Result.result_definition)\
        .filter(ResultGroup.patient == patient)\
        .filter(ResultDefinition.code == result_code)\
        .order_by(ResultGroup.date, Result.id)\
        .all()

    data = []

    for result in results:
        data.append({
            'date': result.result_group.date.isoformat(),
            'value': float(result.value),
            'source': result.result_group.facility.name,
        })

    return jsonify({
        'name': result_definition.name,
        'units': result_definition.units or '',
        'data': data,
    })


@bp.route('/definitions/')
def view_result_definitions(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    result_group_definitions = ResultGroupDefinition.query\
        .order_by(ResultGroupDefinition.name)\
        .all()

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        result_group_definitions=result_group_definitions
    )

    return render_template('patient/result_definitions.html', **context)


class ResultGroupDetailService(PatientDataDetailService):
    def get_object(self, patient, result_group_id):
        result_group = ResultGroup.query\
            .filter(ResultGroup.patient == patient)\
            .filter(ResultGroup.id == result_group_id)\
            .first()
        return result_group

    def new_object(self, patient):
        return ResultGroup(patient=patient)

    def get_form(self, obj, result_group_definition=None):
        if obj.result_group_definition is not None:
            result_group_definition = obj.result_group_definition

        form_class = result_group_to_form(result_group_definition)
        data = result_group_to_form_data(obj)
        return form_class(obj=obj, data=data)


class ResultGroupEditView(PatientDataEditView):
    def __init__(self):
        super(ResultGroupEditView, self).__init__(
            ResultGroupDetailService(current_user),
        )

    def saved(self, patient, obj):
        return redirect(url_for('results.view_result_list', patient_id=patient.id))

    def get_template_name(self):
        return 'patient/result_group_form.html'


class ResultGroupAddView(PatientDataAddView):
    def __init__(self):
        super(ResultGroupAddView, self).__init__(
            ResultGroupDetailService(current_user),
        )

        self.select_form = None

    def get_form(self, obj):
        result_group_definition_id = request.args.get('result_group_definition_id')

        if result_group_definition_id is not None:
            try:
                result_group_definition_id = int(result_group_definition_id)
            except ValueError:
                result_group_definition_id = None

        if result_group_definition_id is None:
            select_form = SelectAddResultGroupForm()
            result_group_choices = get_result_group_choices()
            result_group_choices = add_empty_choice(result_group_choices)
            select_form.result_group_definition_id.choices = result_group_choices
            self.select_form = select_form

            if select_form.validate_on_submit():
                result_group_definition_id = select_form.result_group_definition_id.data

        if result_group_definition_id is not None:
            result_group_definition = ResultGroupDefinition.query.get_or_404(result_group_definition_id)
            obj.result_group_definition = result_group_definition
            obj.result_group_definition_id = result_group_definition.id  # needed for form
            return super(ResultGroupAddView, self).get_form(obj)
        else:
            return None

    def saved(self, patient, obj):
        return redirect(url_for('results.view_result_list', patient_id=patient.id))

    def get_template_name(self):
        return 'patient/result_group_form.html'

    def get_context(self):
        return {
            'select_form': self.select_form
        }


class ResultGroupDeleteView(PatientDataDeleteView):
    def __init__(self):
        super(ResultGroupDeleteView, self).__init__(
            ResultGroupDetailService(current_user),
        )

    def deleted(self, patient):
        return redirect(url_for('results.view_result_list', patient_id=patient.id))


class ResultGroupDetailView(PatientDataDetailView):
    def __init__(self):
        super(ResultGroupDetailView, self).__init__(
            ResultGroupDetailService(current_user),
        )

    def get_template_name(self):
        return 'patient/result_group.html'


bp.add_url_rule('/add/', view_func=ResultGroupAddView.as_view('add_result_group'))
bp.add_url_rule('/<int:result_group_id>/', view_func=ResultGroupDetailView.as_view('view_result_group'))
bp.add_url_rule('/<int:result_group_id>/edit/', view_func=ResultGroupEditView.as_view('edit_result_group'))
bp.add_url_rule('/<int:result_group_id>/delete/', view_func=ResultGroupDeleteView.as_view('delete_result_group'))


@bp.route('/forms/<int:result_group_definition_id>/', methods=['GET', 'POST'])
def result_group_form(patient_id, result_group_definition_id):
    patient = Patient.query.get_or_404(patient_id)

    result_group_definition = ResultGroupDefinition.query.get_or_404(result_group_definition_id)
    form_class = result_group_to_form(result_group_definition)
    result_group = ResultGroup(patient=patient)
    result_group.result_group_definition_id = result_group_definition.id
    form = form_class(obj=result_group)

    context = dict(
        form=form,
        result_group_definition=result_group_definition,
    )

    return render_template('patient/result_group_form_ajax.html', **context)


def get_result_code_choices():
    result_definitions = ResultDefinition.query\
        .order_by(ResultDefinition.name)\
        .all()

    return [(x.code, x.name) for x in result_definitions]


def get_result_group_choices():
    choices = []

    result_group_definitions = ResultGroupDefinition.query\
        .order_by(ResultGroupDefinition.name)\
        .all()

    for x in result_group_definitions:
        choices.append((x.id, x.name))

    return choices
