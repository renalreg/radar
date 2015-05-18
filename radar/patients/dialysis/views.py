from flask import Blueprint, abort, render_template, request, url_for, redirect
from flask_login import current_user
from radar.database import db
from radar.patients.dialysis.forms import DialysisForm
from radar.patients.dialysis.models import Dialysis
from radar.patients.models import Patient
from radar.patients.views import get_patient_data


bp = Blueprint('dialysis', __name__)


@bp.route('/', endpoint='view_dialysis_list')
@bp.route('/', endpoint='add_dialysis', methods=['GET', 'POST'])
@bp.route('/<int:dialysis_id>/', endpoint='view_dialysis')
@bp.route('/<int:dialysis_id>/', endpoint='edit_dialysis', methods=['GET', 'POST'])
def view_dialysis_list(patient_id, dialysis_id=None):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    dialysis_list = Dialysis.query.all()

    if dialysis_id is None:
        dialysis = Dialysis(patient=patient)
    else:
        dialysis = Dialysis.query\
            .filter(Dialysis.patient == patient)\
            .filter(Dialysis.id == dialysis_id)\
            .first_or_404()

    if not dialysis.can_view(current_user):
        abort(403)

    read_only = not dialysis.can_edit(current_user)

    form = DialysisForm(obj=dialysis)

    if request.method == 'POST':
        if read_only:
            abort(403)

        if form.validate():
            dialysis.unit = form.unit_id.obj
            dialysis.date_started = form.date_started.data
            dialysis.date_stopped = form.date_stopped.data
            dialysis.dialysis_type = form.dialysis_type_id.obj

            db.session.add(dialysis)
            db.session.commit()

            return redirect(url_for('dialysis.view_dialysis_list', patient_id=patient_id))

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        dialysis_list=dialysis_list,
        dialysis=dialysis,
        form=form,
        read_only=read_only,
    )

    return render_template('patient/dialysis.html', **context)


@bp.route('/<int:dialysis_id>/delete/')
def delete_dialysis(patient_id, dialysis_id):
    pass