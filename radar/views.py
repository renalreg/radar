from flask import render_template, abort
from flask.views import View

from radar.models import Patient


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