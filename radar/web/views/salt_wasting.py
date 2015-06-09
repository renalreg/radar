from flask import Blueprint, url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from radar.web.forms.salt_wasting import SaltWastingClinicalFeaturesForm
from radar.models.salt_wasting import SaltWastingClinicalFeatures
from radar.web.views.patient_data import PatientDataDetailService, PatientDataDetailView, PatientDataEditView
from radar.web.views.patients import get_patient_data

bp = Blueprint('salt_wasting', __name__)


class SaltWastingClinicalFeaturesDetailService(PatientDataDetailService):
    def get_object(self, patient):
        x = SaltWastingClinicalFeatures.query\
            .filter(SaltWastingClinicalFeatures.patient == patient)\
            .first()
        return x

    def new_object(self, patient):
        return SaltWastingClinicalFeatures(patient=patient)

    def get_form(self, obj):
        return SaltWastingClinicalFeaturesForm(obj=obj)


class SaltWastingClinicalFeaturesDetailView(PatientDataDetailView):
    def __init__(self):
        super(SaltWastingClinicalFeaturesDetailView, self).__init__(
            SaltWastingClinicalFeaturesDetailService(current_user),
        )

    def not_found(self, patient):
        new_obj = self.detail_service.new_object(patient)

        if new_obj.can_edit(current_user):
            return redirect(url_for('salt_wasting.edit_clinical_features', patient_id=patient.id))
        else:
            context = dict(
                patient=patient,
                patient_data=get_patient_data(patient),
            )

            return render_template(self.get_template_name(), **context)

    def get_template_name(self):
        return 'patient/salt_wasting_clinical_features.html'


class SaltWastingClinicalFeaturesEditView(PatientDataEditView):
    create = True

    def __init__(self):
        super(SaltWastingClinicalFeaturesEditView, self).__init__(
            SaltWastingClinicalFeaturesDetailService(current_user),
        )

    def saved(self, patient, obj):
        return redirect(url_for('salt_wasting.view_clinical_features', patient_id=patient.id))

    def get_template_name(self):
        return 'patient/edit_salt_wasting_clinical_features.html'


bp.add_url_rule('/clinical-features/', view_func=SaltWastingClinicalFeaturesDetailView.as_view('view_clinical_features'))
bp.add_url_rule('/clinical-features/edit/', view_func=SaltWastingClinicalFeaturesEditView.as_view('edit_clinical_features'))
