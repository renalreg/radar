from flask import render_template, redirect, url_for
from flask.views import View

from radar.demographics.forms import DemographicsForm

from radar.demographics.models import Demographics
from radar.form_views.detail import SingleFormDetailView
from radar.models import SDAPatient, Patient
from radar.patient_list.views import get_patient_detail_context
from radar.utils import get_path


class DemographicsListView(View):
    def dispatch_request(self, patient_id):
        context = get_patient_detail_context(patient_id)

        sda_patients = SDAPatient.query\
            .join(SDAPatient.sda_resource)\
            .join(Patient)\
            .filter(Patient.id == patient_id)\
            .all()

        demographics_list = []

        for sda_patient in sda_patients:
            demographics = dict()

            demographics['facility'] = sda_patient.sda_resource.facility
            demographics['first_name'] = get_path(sda_patient.data, 'name', 'given_name')
            demographics['last_name'] = get_path(sda_patient.data, 'name', 'family_name')

            demographics_list.append(demographics)

        context['demographics_list'] = demographics_list

        return render_template('patient/demographics.html', **context)

class DemographicsDetailViewView(SingleFormDetailView):
    def get_entry_class(self):
        return Demographics

    def get_form(self, entry):
        return DemographicsForm(obj=entry)

    def get_template_name(self):
        return 'patient/radar_demographics.html'

    def get_success(self, entry):
        return redirect(url_for('patient', patient_id=entry.patient_id))