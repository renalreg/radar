from collections import defaultdict
from flask import Blueprint, render_template, abort, request, url_for, redirect
from flask_login import current_user
from radar.concepts.core import validate_concepts, concepts_to_sda_bundle
from radar.concepts.utils import add_errors_to_form
from radar.database import db
from radar.medications.forms import MedicationForm
from radar.medications.models import Medication
from radar.patients.models import Patient
from radar.patients.views import get_patient_data
from radar.sda.models import SDAMedication, SDABundle
from radar.utils import get_path, get_path_as_datetime

bp = Blueprint('medications', __name__)

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
        medication = dict()
        medication['id'] = sda_medication.id
        medication['name'] = get_path(sda_medication.data, 'order_item', 'description')
        medication['from_date'] = get_path_as_datetime(sda_medication.data, 'from_time')
        medication['to_date'] = get_path_as_datetime(sda_medication.data, 'to_time')

        data_source = sda_medication.sda_bundle.data_source

        if data_source.can_view(current_user):
            medication['view_url'] = data_source.view_url()

        if data_source.can_edit(current_user):
            medication['edit_url'] = data_source.edit_url()

        if data_source.can_edit(current_user):
            medication['delete_url'] = data_source.delete_url()

        medications.append(medication)

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
            form.populate_obj(medication)

            concepts = medication.to_concepts()
            valid, errors = validate_concepts(concepts)

            if valid:
                sda_bundle = concepts_to_sda_bundle(medication.patient, concepts)
                sda_bundle.serialize()
                medication.sda_bundle = sda_bundle
                db.session.add(medication)
                db.session.commit()
                return redirect(url_for('medications.view_medication_list', patient_id=medication.patient.id))
            else:
                add_errors_to_form(form, errors)
                print form.errors

    context = dict(
        patient=medication.patient,
        patient_data=get_patient_data(medication.patient),
        medication=medication,
        form=form
    )

    return render_template('patient/medication.html', **context)


@bp.route('/<int:medication_id>/', endpoint='delete_medication', methods=['POST'])
def delete_medication(medication_id):
    pass