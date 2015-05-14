from flask import Blueprint, abort, render_template, url_for, request
from flask_login import current_user
from radar.database import db
from radar.patients.hospitalisation.forms import HospitalisationForm
from radar.patients.hospitalisation.models import Hospitalisation
from radar.patients.models import Patient
from radar.patients.views import get_patient_data
from werkzeug.utils import redirect


bp = Blueprint('hospitalisation', __name__)


@bp.route('/')
def view_hospitalisation_list(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if not patient.can_view(current_user):
        abort(403)

    hospitalisations = Hospitalisation.query\
        .filter(Hospitalisation.patient == patient)\
        .order_by(Hospitalisation.date_of_admission.desc())\
        .all()

    context = dict(
        patient=patient,
        patient_data=get_patient_data(patient),
        hospitalisations=hospitalisations,
    )

    return render_template('patient/hospitalisations.html', **context)


@bp.route('/add/', endpoint='add_hospitalisation', methods=['GET', 'POST'])
@bp.route('/<int:hospitalisation_id>/', endpoint='view_hospitalisation')
@bp.route('/<int:hospitalisation_id>/', endpoint='edit_hospitalisation', methods=['GET', 'POST'])
def view_hospitalisation(patient_id, hospitalisation_id=None):
    if hospitalisation_id is None:
        patient = Patient.query.get_or_404(patient_id)
        hospitalisation = Hospitalisation(patient=patient)

        if not hospitalisation.can_edit(current_user):
            abort(403)
    else:
        hospitalisation = Hospitalisation.query\
            .filter(Hospitalisation.patient_id == patient_id)\
            .filter(Hospitalisation.id == hospitalisation_id)\
            .with_for_update(read=True)\
            .first_or_404()

    if not hospitalisation.can_view(current_user):
        abort(403)

    read_only = not hospitalisation.can_edit(current_user)

    form = HospitalisationForm(obj=hospitalisation)

    if request.method == 'POST':
        if read_only:
            abort(403)

        if form.validate():
            hospitalisation.unit = form.unit_id.obj
            hospitalisation.date_of_admission = form.date_of_admission.data
            hospitalisation.date_of_discharge = form.date_of_discharge.data
            hospitalisation.reason_for_admission = form.reason_for_admission.data
            hospitalisation.comments = form.comments.data

            db.session.add(hospitalisation)
            db.session.commit()

            return redirect(url_for('hospitalisation.view_hospitalisation_list', patient_id=patient_id))

    context = dict(
        patient=hospitalisation.patient,
        patient_data=get_patient_data(hospitalisation.patient),
        hospitalisation=hospitalisation,
        form=form,
        read_only=read_only,
    )

    return render_template('patient/hospitalisation.html', **context)