from flask import Blueprint, redirect, render_template, url_for, abort, request
from flask_login import current_user

from radar.lib.database import db
from radar.models.patients import Patient
from radar.patients.plasmapheresis.forms import PlasmapheresisForm
from radar.models.plasmapheresis import Plasmapheresis
from radar.views.patients import get_patient_data


bp = Blueprint('plasmapheresis', __name__)


@bp.route('/', endpoint='view_plasmapheresis_list')
@bp.route('/', endpoint='add_plasmapheresis', methods=['GET', 'POST'])
@bp.route('/<int:record_id>/', endpoint='view_plasmapheresis')
@bp.route('/<int:record_id>/', endpoint='edit_plasmapheresis', methods=['GET', 'POST'])
def view_plasmapheresis_list(patient_id, record_id=None):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    records = Plasmapheresis.query.all()

    if record_id is None:
        record = Plasmapheresis(patient=patient)
    else:
        record = Plasmapheresis.query\
            .filter(Plasmapheresis.patient == patient)\
            .filter(Plasmapheresis.id == record_id)\
            .first_or_404()

    if not record.can_view(current_user):
        abort(403)

    read_only = not record.can_edit(current_user)

    form = PlasmapheresisForm(obj=record)

    if request.method == 'POST':
        if read_only:
            abort(403)

        if form.validate():
            record.unit = form.unit_id.obj
            record.from_date = form.from_date.data
            record.to_date = form.to_date.data
            record.no_of_exchanges = form.no_of_exchanges.data
            record.response = form.response_id.obj

            db.session.add(record)
            db.session.commit()

            return redirect(url_for('plasmapheresis.view_plasmapheresis_list', patient_id=patient_id))

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        records=records,
        record=record,
        form=form,
        read_only=read_only,
    )

    return render_template('patient/plasmapheresis.html', **context)