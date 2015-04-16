from flask import render_template, request

from flask.views import View
from flask_login import current_user

from radar.patients.forms import PatientSearchFormHandler
from radar.services import get_patients_for_user, get_units_for_user, get_disease_groups_for_user


class PatientListView(View):
    def dispatch_request(self):
        search = {}
        form = PatientSearchFormHandler(search)
        form.submit(request.args)

        patients = get_patients_for_user(current_user, search)

        unit_choices = [(x.name, x.id) for x in get_units_for_user(current_user)]
        disease_group_choices = [(x.name, x.id) for x in get_disease_groups_for_user(current_user)]

        return render_template(
            'patients.html',
            patients=patients,
            form=form,
            unit_choices=unit_choices,
            disease_group_choices=disease_group_choices
        )