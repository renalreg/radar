from flask import render_template, Blueprint, redirect, url_for
from flask.views import View
from radar.demographics.forms import DemographicsForm

from radar.demographics.models import Demographics
from radar.form_views.detail import SingleFormDetail
from radar.models import SDAPatient, Patient
from radar.patients.views import get_patient_detail_context
from radar.utils import get_path


class DemographicsList(View):
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

        return render_template('patient/demographics/list.html', **context)

class DemographicsDetail(SingleFormDetail):
    def get_entry_class(self):
        return Demographics

    def get_form(self, entry):
        return DemographicsForm(obj=entry)

    def get_template_name(self):
        return 'patient/demographics/detail.html'

    def get_success(self, entry):
        return redirect(url_for('demographics.list', patient_id=entry.patient_id))

app = Blueprint('demographics', __name__)

app.add_url_rule('/', view_func=DemographicsList.as_view('list'))
app.add_url_rule('/demographics/', view_func=DemographicsDetail.as_view('detail'))
app.add_url_rule('/demographics/', view_func=DemographicsDetail.as_view('update'))