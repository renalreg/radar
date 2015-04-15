from flask import render_template, abort, request, redirect, url_for, flash
from flask.views import View
from flask_login import login_user, logout_user

from radar.models import Patient, User


class PatientsView(View):
    def dispatch_request(self):
        patients = Patient.query.all()
        return render_template('patients.html', patients=patients)

class PatientView(View):
    def dispatch_request(self, patient_id):
        patient = Patient.query.filter(Patient.id == patient_id).first()

        if patient is None:
            abort(404)

        return render_template('patient.html', patient=patient)

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
                flash('Logged in successfully.')
                return redirect(request.args.get('next') or url_for('index'))
            else:
                login_failed = True

        return render_template('login.html', username=username, login_failed=login_failed)

class LogoutView(View):
    def dispatch_request(self):
        logout_user()
        return redirect(url_for('index'))