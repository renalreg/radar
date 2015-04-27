from flask import redirect, url_for

from radar.diagnoses.forms import DiagnosisForm
from radar.diagnoses.models import Diagnosis

from radar.form_views.detail import SingleFormDetailView


class DiagnosisDetailView(SingleFormDetailView):
    def __init__(self):
        super(SingleFormDetailView, self).__init__(per_disease_group=True)

    def get_entry_class(self):
        return Diagnosis

    def get_form(self, entry):
        return DiagnosisForm(obj=entry)

    def get_template_name(self):
        return 'patient/diagnosis.html'

    def get_success(self, entry):
        return redirect(url_for('patient', patient_id=entry.patient_id))