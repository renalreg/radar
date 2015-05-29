from flask import Blueprint, abort, request, redirect, url_for, render_template
from flask_login import current_user

from radar.lib.database import db
from radar.models.patients import Patient
from radar.lib.forms.salt_wasting import SaltWastingClinicalFeaturesForm
from radar.models.salt_wasting import SaltWastingClinicalFeatures
from radar.views.patients import get_patient_data


bp = Blueprint('salt_wasting', __name__)


@bp.route('/clinical-features/')
@bp.route('/clinical-features/', endpoint='edit_clinical_features', methods=['GET', 'POST'])
def view_clinical_features(patient_id):
    record = SaltWastingClinicalFeatures.query\
        .filter(SaltWastingClinicalFeatures.patient_id == patient_id)\
        .first()

    if record is None:
        patient = Patient.query.get_or_404(patient_id)
        record = SaltWastingClinicalFeatures(patient=patient)

    if not record.can_view(current_user):
        abort(403)

    read_only = not record.can_edit(current_user)

    form = SaltWastingClinicalFeaturesForm(obj=record)

    if request.method == 'POST':
        if read_only:
            abort(403)

        if form.validate():
            form.populate_obj(record)
            db.session.add(record)
            db.session.commit()
            return redirect(url_for('salt_wasting.view_clinical_features', patient_id=patient_id))

    context = dict(
        patient=record.patient,
        patient_data=get_patient_data(record.patient),
        form=form,
        read_only=read_only,
    )

    return render_template('patient/salt_wasting_clinical_features.html', **context)