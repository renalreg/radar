from flask import render_template, request, abort
from flask.views import View
from flask_login import current_user
from radar.pagination import Pagination
from radar.patient_list.forms import PatientSearchForm, PER_PAGE_DEFAULT, PER_PAGE_CHOICES, ORDER_BY_CHOICES

from radar.patient_list.search import PatientQueryBuilder
from radar.services import get_unit_filters_for_user, get_disease_group_filters_for_user, \
    filter_patient_disease_groups_for_user, filter_patient_units_for_user, get_patient_for_user, \
    can_user_view_demographics, can_user_view_patient_demographics, can_user_list_patients
from radar.views import get_base_context


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
        if not can_user_list_patients(current_user):
            abort(403)

        context = get_patient_base_context()

        form = PatientSearchForm(formdata=request.args, csrf_enabled=False)

        disease_group_choices = [(x.id, x.name) for x in get_disease_group_filters_for_user(current_user)]
        disease_group_choices.insert(0, ('', ''))
        form.disease_group_id.choices = disease_group_choices

        unit_choices = [(x.id, x.name) for x in get_unit_filters_for_user(current_user)]
        unit_choices.insert(0, ('', ''))
        form.unit_id.choices = unit_choices

        builder = PatientQueryBuilder(current_user)

        if form.validate():
            if form.first_name.data:
                builder.first_name(form.first_name.data)

            if form.last_name.data:
                builder.last_name(form.last_name.data)

            if form.unit_id.data:
                builder.unit(form.unit_id.data)

            if form.disease_group_id.data:
                builder.disease_group(form.disease_group_id.data)

            if form.date_of_birth.data:
                builder.date_of_birth(form.date_of_birth.data)

            if form.patient_number.data:
                builder.patient_number(form.patient_number.data)

            if form.gender.data:
                builder.gender(form.gender.data)

            if form.radar_id.data:
                builder.radar_id(form.radar_id.data)

            if form.year_of_birth.data:
                builder.year_of_birth(form.year_of_birth.data)

            builder.order_by(form.order_by.data, form.order_direction.data == 'asc')

        query = builder.build()

        page = form.page.data or 1
        per_page = form.per_page.data or PER_PAGE_DEFAULT
        count = query.count()

        pagination = Pagination(page, per_page, count)

        if per_page >= 0:
            query = query.offset(per_page * (page - 1)).limit(per_page)

        patients = query.all()

        # Get demographics permissions for each patient
        patients = [(p, can_user_view_patient_demographics(current_user, p)) for p in patients]

        context.update({
            'patients': patients,
            'form': form,
            'unit_choices': unit_choices,
            'disease_group_choices': disease_group_choices,
            'demographics': can_user_view_demographics(current_user),
            'pagination': pagination,
            'per_page_choices': PER_PAGE_CHOICES,
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