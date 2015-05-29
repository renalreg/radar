from flask import Blueprint, render_template, abort, request, url_for, redirect
from flask_login import current_user

from radar.lib.concepts.utils import add_errors_to_form
from radar.lib.database import db
from radar.lib.forms.common import DeleteForm
from radar.lib.forms.medications import MedicationForm
from radar.models.medications import Medication
from radar.models.patients import Patient
from radar.views.patients import get_patient_data
from radar.lib.sda.models import SDAMedication, SDABundle
from radar.lib.utils import get_path_as_text, get_path_as_datetime


bp = Blueprint('medications', __name__)


class MedicationProxy(object):
    def __init__(self, sda_medication):
        self.sda_medication = sda_medication

    @property
    def id(self):
        return self.sda_medication.id

    @property
    def name(self):
        return get_path_as_text(self.sda_medication.data, ['order_item', 'description'])

    @property
    def from_date(self):
        return get_path_as_datetime(self.sda_medication.data, ['from_time'])

    @property
    def to_date(self):
        return get_path_as_datetime(self.sda_medication.data, ['to_time'])

    @property
    def dose_quantity(self):
        return get_path_as_text(self.sda_medication.data, ['dose_quantity'])

    @property
    def dose_unit(self):
        return get_path_as_text(self.sda_medication.data, ['dose_uom', 'description'])

    @property
    def frequency(self):
        return get_path_as_text(self.sda_medication.data, ['frequency', 'description'])

    @property
    def route(self):
        return get_path_as_text(self.sda_medication.data, ['route', 'description'])

    @property
    def source(self):
        return get_path_as_text(self.sda_medication.data, ['entering_organization', 'description'])

    @property
    def _data_source(self):
        return self.sda_medication.sda_bundle.data_source

    @property
    def view_url(self):
        if self._data_source.can_view(current_user):
            return self._data_source.view_url()
        else:
            return None

    @property
    def edit_url(self):
        if self._data_source.can_edit(current_user):
            return self._data_source.view_url()
        else:
            return None

    @property
    def delete_url(self):
        if self._data_source.can_edit(current_user):
            return self._data_source.view_url()
        else:
            return None


@bp.route('/')
def view_medication_list(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    sda_medications = SDAMedication.query\
        .join(SDAMedication.sda_bundle)\
        .join(SDABundle.patient)\
        .filter(Patient.id == patient_id)\
        .order_by(SDAMedication.data['from_time'].desc())\
        .all()

    medications = []

    for sda_medication in sda_medications:
        medication_proxy = MedicationProxy(sda_medication)
        medications.append(medication_proxy)

    context = dict(
        medications=medications,
        patient=patient,
        patient_data=get_patient_data(patient)
    )

    return render_template('patient/medications.html', **context)


@bp.route('/new/', endpoint='add_medication', methods=['GET', 'POST'])
@bp.route('/<int:medication_id>/', endpoint='view_medication')
@bp.route('/<int:medication_id>/', endpoint='edit_medication', methods=['GET', 'POST'])
def view_medication(patient_id, medication_id=None):
    if medication_id is None:
        patient = Patient.query.get_or_404(patient_id)
        medication = Medication(patient=patient)

        if not medication.can_edit(current_user):
            abort(403)
    else:
        medication = Medication.query\
            .filter(Medication.patient_id == patient_id)\
            .filter(Medication.id == medication_id)\
            .with_for_update(read=True)\
            .first_or_404()

    if not medication.can_view(current_user):
        abort(403)

    read_only = not medication.can_edit(current_user)

    form = MedicationForm(obj=medication)

    if request.method == 'POST':
        if read_only:
            abort(403)

        if form.validate():
            medication.unit = form.unit_id.obj
            medication.from_date = form.from_date.data
            medication.to_date = form.to_date.data
            medication.name = form.name.data
            medication.dose_quantity = form.dose_quantity.data
            medication.dose_unit = form.dose_unit_id.obj
            medication.frequency = form.frequency_id.obj
            medication.route = form.route_id.obj

            concept_map = medication.to_concepts()
            valid, errors = concept_map.validate()

            if valid:
                db.session.add(medication)
                db.session.commit()
                return redirect(url_for('medications.view_medication_list', patient_id=medication.patient.id))
            else:
                form.add_errors(errors)

    context = dict(
        patient=medication.patient,
        patient_data=get_patient_data(medication.patient),
        medication=medication,
        form=form,
        read_only=read_only,
    )

    return render_template('patient/medication.html', **context)


@bp.route('/<int:medication_id>/delete/', endpoint='delete_medication', methods=['POST'])
def delete_medication(patient_id, medication_id):
    medication = Medication.query\
        .filter(Medication.id == medication_id)\
        .filter(Medication.patient_id == patient_id)\
        .first_or_404()

    form = DeleteForm()

    if not medication.can_edit(current_user) or not form.validate_on_submit():
        abort(403)

    db.session.delete(medication)
    db.session.commit()

    return redirect(url_for('medications.view_medication_list', patient_id=patient_id))