from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user

from radar.lib.database import db
from radar.models.patients import Patient
from radar.lib.forms.transplants import TransplantForm
from radar.models.transplants import Transplant
from radar.views.patients import get_patient_data


bp = Blueprint('transplants', __name__)


@bp.route('/', endpoint='view_transplant_list')
@bp.route('/', endpoint='add_transplant', methods=['GET', 'POST'])
@bp.route('/<int:transplant_id>/', endpoint='view_transplant')
@bp.route('/<int:transplant_id>/', endpoint='edit_transplant', methods=['GET', 'POST'])
def view_transplant_list(patient_id, transplant_id=None):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    transplants = Transplant.query.all()

    if transplant_id is None:
        transplant = Transplant(patient=patient)
    else:
        transplant = Transplant.query\
            .filter(Transplant.patient == patient)\
            .filter(Transplant.id == transplant_id)\
            .first_or_404()

    if not transplant.can_view(current_user):
        abort(403)

    read_only = not transplant.can_edit(current_user)

    form = TransplantForm(obj=transplant)

    if request.method == 'POST':
        if read_only:
            abort(403)

        if form.validate():
            transplant.unit = form.unit_id.obj
            transplant.transplant_date = form.transplant_date.data
            transplant.transplant_type = form.transplant_type_id.obj
            transplant.reoccurred = form.reoccurred.data
            transplant.date_reoccurred = form.date_reoccurred.data
            transplant.date_failed = form.date_failed.data

            db.session.add(transplant)
            db.session.commit()

            return redirect(url_for('transplants.view_transplant_list', patient_id=patient_id))

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        transplants=transplants,
        transplant=transplant,
        form=form,
        read_only=read_only,
    )

    return render_template('patient/transplants.html', **context)