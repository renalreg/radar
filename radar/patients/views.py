from flask import render_template, request, abort
from flask.views import View
from flask_login import current_user

from radar.patients.forms import PatientSearchFormHandler
from radar.services import get_patients_for_user, get_unit_filters_for_user, get_disease_group_filters_for_user, \
    filter_patient_disease_groups_for_user, filter_patient_units_for_user, get_patient_for_user, \
    can_user_view_demographics
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
    context['demographics'] = can_user_view_demographics(current_user, patient)

    return context

class PatientListView(View):
    def dispatch_request(self):
        search = {}
        form = PatientSearchFormHandler(search)
        form.submit(request.args)

        patients = get_patients_for_user(current_user, search)

        unit_choices = [(x.name, x.id) for x in get_unit_filters_for_user(current_user)]
        disease_group_choices = [(x.name, x.id) for x in get_disease_group_filters_for_user(current_user)]

        context = get_patient_base_context()
        context.update({
            'patients': patients,
            'form': form,
            'unit_choices': unit_choices,
            'disease_group_choices': disease_group_choices,
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