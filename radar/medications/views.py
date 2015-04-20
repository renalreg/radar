from flask import Blueprint

from radar.form_views import FormDeleteView, FormDetailView, FormListView
from radar.medications.models import Medication
from radar.medications.forms import MedicationFormHandler


class MedicationListView(FormListView):
    model = Medication

class MedicationDetailView(FormDetailView):
    model = Medication
    form_handler = MedicationFormHandler

class MedicationDeleteView(FormDeleteView):
    model = Medication

app = Blueprint('medications', __name__)
app.add_url_rule('/', view_func=MedicationListView.as_view('list', 'patient/medications/list.html'))
app.add_url_rule('/new', 'create', view_func=MedicationDetailView.as_view('create', 'patient/medications/detail.html'))
app.add_url_rule('/<int:form_entry_id>/', view_func=MedicationDetailView.as_view('detail', 'patient/medications/detail.html'))
app.add_url_rule('/<int:form_entry_id>/', view_func=MedicationDetailView.as_view('update', 'patient/medications/detail.html'))
app.add_url_rule('/<int:form_entry_id>/delete', view_func=MedicationDeleteView.as_view('delete'))