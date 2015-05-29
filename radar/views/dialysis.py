from flask import Blueprint, abort, render_template, request, url_for, redirect
from flask_login import current_user

from radar.concepts.core import concepts_to_sda_bundle, validate_concepts
from radar.concepts.utils import add_errors_to_form
from radar.lib.database import db
from radar.patients.dialysis.forms import DialysisForm
from radar.models.dialysis import Dialysis
from radar.models.patients import Patient
from radar.views.patients import get_patient_data


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
            dialysis.from_date = form.from_date.data
            dialysis.to_date = form.to_date.data
            dialysis.dialysis_type = form.dialysis_type_id.obj

            concepts = dialysis.to_concepts()
            valid, errors = validate_concepts(concepts)

            if valid:
                sda_bundle = concepts_to_sda_bundle(concepts, dialysis.patient)
                sda_bundle.serialize()
                dialysis.sda_bundle = sda_bundle
                db.session.add(dialysis)
                db.session.commit()
                return redirect(url_for('dialysis.view_dialysis_list', patient_id=patient_id))
            else:
                add_errors_to_form(form, errors)

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
    # TODO
    pass