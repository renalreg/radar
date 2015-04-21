from flask import render_template, request, abort
from flask.views import View
from flask_login import current_user
from radar.pagination import Pagination

from radar.patients.forms import PatientSearchFormHandler
from radar.patients.search import get_patients_for_user_query
from radar.services import get_unit_filters_for_user, get_disease_group_filters_for_user, \
    filter_patient_disease_groups_for_user, filter_patient_units_for_user, get_patient_for_user, \
    can_user_view_demographics, can_user_view_patient_demographics
from radar.views import get_base_context

PER_PAGE_CHOICES = [('10', 10), ('25', 25), ('50', 50), ('100', 100), ('All', -1)]
PER_PAGE_DEFAULT = 50
ORDER_BY_CHOICES = [
    ('RaDaR ID', 'radar_id'),
    ('First Name', 'first_name'),
    ('Last Name', 'last_name'),
    ('Date of Birth', 'date_of_birth'),
    ('Gender', 'gender'),
]

def get_patient_base_context():
    context = get_base_context()

    context.update({
        'filter_patient_units_for_user': filter_patient_units_for_user,
        'filter_patient_disease_groups_for_user': filter_patient_disease_groups_for_user,
    })

    return context

def get_patient_detail_context(patient_id):
    context = get_patient_base_context()

    patient = get_patient_for_user(current_user, patient_id)

    if patient is None:
        abort(404)

    context['patient'] = patient
    context['patient_demographics'] = can_user_view_patient_demographics(current_user, patient)

    return context

class PatientListView(View):
    def dispatch_request(self):
        context = get_patient_base_context()

        params = {}
        form = PatientSearchFormHandler(params)
        form.submit(request.args)

        query = get_patients_for_user_query(current_user, params)

        if params.get('per_page') is None:
            params['per_page'] = PER_PAGE_DEFAULT

        page = params.get('page') or 1
        per_page = params.get('per_page')
        count = query.count()

        pagination = Pagination(page, per_page, count)

        if per_page >= 0:
            query = query.offset(per_page * (page - 1)).limit(per_page)

        patients = query.all()

        # Get demographics permissions for each patient
        patients = [(p, can_user_view_patient_demographics(current_user, p)) for p in patients]

        unit_choices = [(x.name, x.id) for x in get_unit_filters_for_user(current_user)]
        disease_group_choices = [(x.name, x.id) for x in get_disease_group_filters_for_user(current_user)]

        context.update({
            'patients': patients,
            'form': form,
            'unit_choices': unit_choices,
            'disease_group_choices': disease_group_choices,
            'demographics': can_user_view_demographics(current_user),
            'per_page_choices': PER_PAGE_CHOICES,
            'pagination': pagination,
            'order_by_choices': ORDER_BY_CHOICES,
        })

        return render_template('patients.html', **context)

class PatientDiseaseGroupsView(View):
    def dispatch_request(self, patient_id):
        context = get_patient_detail_context(patient_id)
        return render_template('patient/disease_groups.html', **context)

class PatientUnitsView(View):
    def dispatch_request(self, patient_id):
        context = get_patient_detail_context(patient_id)
        return render_template('patient/units.html', **context)