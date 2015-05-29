from flask import Blueprint, abort, render_template, request, url_for
from flask_login import current_user
from werkzeug.utils import redirect

from radar.lib.database import db
from radar.models.patients import Patient
from radar.views.patients import get_patient_data
from radar.patients.renal_imaging.forms import RenalImagingForm
from radar.models.renal_imaging import RenalImaging


bp = Blueprint('renal_imaging', __name__)


@bp.route('/')
def view_result_list(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    results = RenalImaging.query.order_by(RenalImaging.date.desc(), RenalImaging.imaging_type).all()

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        results=results,
    )

    return render_template('patient/renal_imaging_list.html', **context)


@bp.route('/new/', endpoint='add_result', methods=['GET', 'POST'])
@bp.route('/<int:result_id>/', endpoint='view_result')
@bp.route('/<int:result_id>/', endpoint='edit_result', methods=['GET', 'POST'])
def view_result(patient_id, result_id=None):
    if result_id is None:
        patient = Patient.query.get_or_404(patient_id)
        result = RenalImaging(patient=patient)
    else:
        result = RenalImaging.query\
            .filter(RenalImaging.patient_id == patient_id)\
            .filter(RenalImaging.id == result_id)\
            .first_or_404()

    if not result.can_view(current_user):
        abort(403)

    read_only = not result.can_edit(current_user)

    form = RenalImagingForm(obj=result)

    if request.method == 'POST':
        if read_only:
            abort(403)

        if form.validate():
            form.populate_obj(result)
            db.session.add(result)
            db.session.commit()
            return redirect(url_for('renal_imaging.view_result_list', patient_id=patient_id))

    context = dict(
        patient=result.patient,
        patient_data=get_patient_data(result.patient),
        form=form,
        result=result,
        read_only=read_only
    )

    return render_template('patient/renal_imaging.html', **context)