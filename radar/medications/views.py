from flask import Blueprint, render_template, url_for, redirect
from flask.views import View

from radar.database import db_session
from radar.form_services import sda_resource_to_edit_url, sda_resource_to_delete_url
from radar.medications.forms import MedicationForm
from radar.medications.models import Medication
from radar.models import SDAMedication, SDAResource, Patient
from radar.patients.views import get_patient_detail_context
from radar.utils import get_path_as_datetime, get_path
from radar.form_views.detail import RepeatingFormDetail
from radar.form_views.delete import RepeatingFormDelete


class MedicationList(View):
    def dispatch_request(self, patient_id):
        context = get_patient_detail_context(patient_id)

        medications = list()

        sda_medications = db_session.query(SDAMedication)\
            .join(SDAMedication.sda_resource)\
            .join(SDAResource.patient)\
            .filter(Patient.id == patient_id)\
            .order_by(SDAMedication.data['from_time'].desc())\
            .all()

        for sda_medication in sda_medications:
            medication = dict()
            medication['id'] = sda_medication.id
            medication['name'] = get_path(sda_medication.data, 'order_item', 'description')
            medication['from_date'] = get_path_as_datetime(sda_medication.data, 'from_time')
            medication['to_date'] = get_path_as_datetime(sda_medication.data, 'to_time')
            medication['edit_url'] = sda_resource_to_edit_url(sda_medication.sda_resource)
            medication['delete_url'] = sda_resource_to_delete_url(sda_medication.sda_resource)
            medications.append(medication)

        context['medications'] = medications

        return render_template('patient/medications/list.html', **context)


class MedicationDetail(RepeatingFormDetail):
    def get_entry_class(self):
        return Medication

    def get_form(self, entry):
        return MedicationForm(obj=entry)

    def validate(self, form, entry):
        if entry.to_date is not None and entry.from_date > entry.to_date:
            form.to_date.errors.append('To date must be on or after from date.')

        return not form.errors

    def get_template_name(self):
        return 'patient/medications/detail.html'

    def get_success(self, entry):
        return redirect(url_for('medications.list', patient_id=entry.patient_id))


class MedicationDelete(RepeatingFormDelete):
    def get_entry_class(self):
        return Medication

    def success(self, patient):
        return redirect(url_for('medications.list', patient_id=patient.id))


app = Blueprint('medications', __name__)
app.add_url_rule('/', view_func=MedicationList.as_view('list'))
app.add_url_rule('/new', 'create', view_func=MedicationDetail.as_view('create'))
app.add_url_rule('/<int:entry_id>/', view_func=MedicationDetail.as_view('detail'))
app.add_url_rule('/<int:entry_id>/', view_func=MedicationDetail.as_view('update'))
app.add_url_rule('/<int:entry_id>/delete', view_func=MedicationDelete.as_view('delete'))