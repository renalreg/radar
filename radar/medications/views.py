from flask import Blueprint, render_template, url_for
from flask.views import View

from radar.form_views import FormDeleteView, FormDetailView
from radar.medications.models import Medication
from radar.medications.forms import MedicationFormHandler
from radar.models import SDAMedication
from radar.patients.views import get_patient_detail_context
from radar.utils import get_path_as_datetime, get_path

class MedicationListView(View):
    def dispatch_request(self, patient_id):
        context = get_patient_detail_context(patient_id)

        medications = list()

        for sda_medication in SDAMedication.query.order_by(SDAMedication.data['from_time'].desc()).all():
            medication = dict()
            medication['id'] = sda_medication.id
            medication['name'] = get_path(sda_medication.data, 'order_item', 'description')
            medication['from_date'] = get_path_as_datetime(sda_medication.data, 'from_time')
            medication['to_date'] = get_path_as_datetime(sda_medication.data, 'to_time')

            resource = sda_medication.sda_container.resource

            if resource.type == 'medications':
                medication['edit_url'] = url_for('medications.update', patient_id=patient_id, resource_id=resource.id)
                medication['delete_url'] = url_for('medications.delete', patient_id=patient_id, resource_id=resource.id)

            medications.append(medication)

        context['medications'] = medications

        return render_template('patient/medications/list.html', **context)

class MedicationDetailView(FormDetailView):
    model = Medication
    form_handler = MedicationFormHandler

class MedicationDeleteView(FormDeleteView):
    model = Medication

app = Blueprint('medications', __name__)
app.add_url_rule('/', view_func=MedicationListView.as_view('list'))
app.add_url_rule('/new', 'create', view_func=MedicationDetailView.as_view('create', 'patient/medications/detail.html'))
app.add_url_rule('/<int:resource_id>/', view_func=MedicationDetailView.as_view('detail', 'patient/medications/detail.html'))
app.add_url_rule('/<int:resource_id>/', view_func=MedicationDetailView.as_view('update', 'patient/medications/detail.html'))
app.add_url_rule('/<int:resource_id>/delete', view_func=MedicationDeleteView.as_view('delete'))