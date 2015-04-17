from flask import render_template, abort, request, redirect, url_for, flash
from flask.views import View
from flask_login import login_user, logout_user, current_user
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from radar.database import db_session

from radar.models import Patient, User, UnitPatient, Unit, UnitUser, DiseaseGroupPatient, DiseaseGroup, DiseaseGroupUser
from radar.services import get_disease_groups_for_user, get_units_for_user, get_unit_for_user, \
    get_disease_group_for_user


class BaseView(View):
    def get_context(self):
        context = dict()
        context['units'] = get_units_for_user(current_user)
        context['disease_groups'] = get_disease_groups_for_user(current_user)
        return context

class DemographicsView(View):
    def dispatch_request(self, patient_id):
        patient = Patient.query.filter(Patient.id == patient_id).first()

        if patient is None:
            abort(404)

        return render_template('demographics.html', patient=patient)

class IndexView(View):
    def dispatch_request(self):
        return render_template('index.html')

class LoginView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        username = ""
        login_failed = False

        if request.method == 'POST':
            username = request.form.get('username', '')
            password = request.form.get('password', '')

            user = User.query.filter(User.username == username).first()

            if user is not None and user.check_password(password):
                login_user(user)
                flash('Logged in successfully.', 'success')
                return redirect(request.args.get('next') or url_for('index'))
            else:
                login_failed = True

        return render_template('login.html', username=username, login_failed=login_failed)

class LogoutView(View):
    def dispatch_request(self):
        logout_user()
        return redirect(url_for('index'))

class DiseaseGroupsView(BaseView):
    def dispatch_request(self):
        context = self.get_context()
        return render_template('disease_groups.html', **context)

class DiseaseGroupView(BaseView):
    def dispatch_request(self, disease_group_id):
        disease_group = get_disease_group_for_user(current_user, disease_group_id)

        if disease_group is None:
            abort(404)

        context = self.get_context()
        context['disease_group'] = disease_group

        return render_template('disease_group.html', **context)

class UnitsView(BaseView):
    def dispatch_request(self):
        context = self.get_context()
        return render_template('units.html', **context)

class UnitView(BaseView):
    def dispatch_request(self, unit_id):
        unit = get_unit_for_user(current_user, unit_id)

        if unit is None:
            abort(404)

        context = self.get_context()
        context['unit'] = unit

        return render_template('unit.html', **context)