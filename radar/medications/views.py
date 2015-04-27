from flask import Blueprint, render_template, url_for, redirect
from flask.views import View

from radar.database import db_session
from radar.form_services import sda_resource_to_update_url, sda_resource_to_delete_url
from radar.medications.forms import MedicationForm
from radar.medications.models import Medication
from radar.models import SDAMedication, SDAResource, Patient
from radar.patient_list.views import get_patient_detail_context
from radar.utils import get_path_as_datetime, get_path
from radar.form_views.detail import RepeatingFormDetailView
from radar.form_views.delete import RepeatingFormDeleteView


class MedicationListView(View):
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
            medication['update_url'] = sda_resource_to_update_url(sda_medication.sda_resource)
            medication['delete_url'] = sda_resource_to_delete_url(sda_medication.sda_resource)
            medications.append(medication)

        context['medications'] = medications

        return render_template('patient/medications.html', **context)


class MedicationDetailView(RepeatingFormDetailView):
    def get_entry_class(self):
        return Medication

    def get_form(self, entry):
        return MedicationForm(obj=entry)

    def validate(self, form, entry):
        if entry.to_date is not None and entry.from_date > entry.to_date:
            form.to_date.errors.append('To date must be on or after from date.')

        return not form.errors

    def get_template_name(self):
        return 'patient/medication.html'

    def get_success(self, entry):
        return redirect(url_for('medications', patient_id=entry.patient_id))


class MedicationDeleteView(RepeatingFormDeleteView):
    def get_entry_class(self):
        return Medication

    def success(self, patient):
        return redirect(url_for('medications', patient_id=patient.id))