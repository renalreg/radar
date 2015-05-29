from flask import Blueprint, render_template, abort, request, url_for, redirect, flash
from flask_login import current_user

from radar.lib.database import db
from radar.lib.forms.common import DeleteForm
from radar.lib.forms.medications import MedicationForm
from radar.models.medications import Medication
from radar.models.patients import Patient
from radar.views.patients import get_patient_data

bp = Blueprint('medications', __name__)


@bp.route('/', endpoint='view_medication_list')
@bp.route('/', endpoint='add_medication', methods=['GET', 'POST'])
@bp.route('/<int:medication_id>/edit/', endpoint='edit_medication', methods=['GET', 'POST'])
def view_medications(patient_id, medication_id=None):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    medications = Medication.query\
        .filter(Medication.patient == patient)\
        .order_by(Medication.from_date.desc(), Medication.to_date.desc(), Medication.name.asc())\
        .all()

    medication = None
    form = None

    if medication_id is not None:
        medication = Medication.query\
            .filter(Medication.patient == patient)\
            .filter(Medication.id == medication_id)\
            .first_or_404()

        if not medication.can_edit(current_user):
            abort(403)
    elif patient.can_edit(current_user):
        medication = Medication(patient=patient)

    if medication is not None:
        form = MedicationForm(obj=medication)

    if request.method == 'POST':
        if medication is None:
            abort(403)

        if form.validate():
            medication.facility = form.facility_id.obj
            medication.from_date = form.from_date.data
            medication.to_date = form.to_date.data
            medication.name = form.name.data
            medication.dose_quantity = form.dose_quantity.data
            medication.dose_unit = form.dose_unit_id.obj
            medication.frequency = form.frequency_id.obj
            medication.route = form.route_id.obj

            concept_map = medication.concept_map()
            valid, errors = concept_map.validate()

            if valid:
                db.session.add(medication)
                db.session.commit()
                flash('Saved.', 'success')
                return redirect(url_for('medications.view_medication_list', patient_id=medication.patient.id))
            else:
                form.add_errors(errors)

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        medications=medications,
        medication=medication,
        form=form,
    )

    return render_template('patient/medications.html', **context)


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