from flask import Blueprint, render_template, abort, url_for
from flask_login import current_user
from radar.database import db
from radar.disease_groups.models import DiseaseGroup
from radar.patients.genetics.forms import GeneticsForm
from radar.patients.genetics.models import Genetics
from radar.patients.models import Patient
from radar.patients.views import get_patient_data
from werkzeug.utils import redirect


bp = Blueprint('genetics', __name__)


@bp.route('/<int:disease_group_id>', endpoint='view_genetics')
@bp.route('/<int:disease_group_id>', endpoint='edit_genetics', methods=['GET', 'POST'])
def view_genetics(patient_id, disease_group_id):
    genetics = Genetics.query\
        .filter(Genetics.patient_id == patient_id)\
        .filter(Genetics.disease_group_id == disease_group_id)\
        .first()

    if genetics is None:
        patient = Patient.query.get_or_404(patient_id)
        disease_group = DiseaseGroup.query.get_or_404(disease_group_id)

        genetics = Genetics(
            patient=patient,
            disease_group=disease_group,
        )

    if not genetics.can_view(current_user):
        abort(403)

    read_only = not genetics.can_edit(current_user)

    form = GeneticsForm(obj=genetics, sample_sent=(genetics is not None))

    if form.validate_on_submit():
        if read_only:
            abort(403)

        if form.sample_sent.data:
            form.populate_obj(genetics)

            db.session.add(genetics)
            db.session.commit()
        else:
            if genetics.id:
                db.session.delete(genetics)
                db.session.commit()

        return redirect(url_for('genetics.view_genetics', patient_id=patient_id, disease_group_id=disease_group_id))

    context = dict(
        patient=genetics.patient,
        patient_data=get_patient_data(genetics.patient),
        disease_group=genetics.disease_group,
        form=form,
        read_only=read_only,
    )

    return render_template('patient/genetics.html', **context)