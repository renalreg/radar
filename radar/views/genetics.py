from flask import Blueprint, url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from radar.lib.forms.genetics import GeneticsForm
from radar.lib.validation.core import FormErrorHandler
from radar.lib.validation.genetics import validate_genetics
from radar.models.genetics import Genetics
from radar.views.patient_data import DetailService, PatientDataDetailView, PatientDataEditView
from radar.views.patients import get_patient_data


bp = Blueprint('genetics', __name__)


class GeneticsDetailService(DetailService):
    def get_object(self, patient, disease_group):
        genetics = Genetics.query\
            .filter(Genetics.patient == patient)\
            .filter(Genetics.disease_group == disease_group)\
            .first()
        return genetics

    def new_object(self, patient, disease_group):
        return Genetics(patient=patient, disease_group=disease_group)

    def get_form(self, obj):
        return GeneticsForm(obj=obj)

    def validate(self, form, obj):
        errors = FormErrorHandler(form)
        validate_genetics(errors, obj)
        return errors.is_valid()


class GeneticsDetailView(PatientDataDetailView):
    disease_group = True

    def __init__(self):
        super(GeneticsDetailView, self).__init__(
            GeneticsDetailService(current_user),
        )

    def not_found(self, patient, disease_group):
        new_obj = self.detail_service.new_object(patient, disease_group)

        if new_obj.can_edit(current_user):
            return redirect(url_for('genetics.edit_genetics', patient_id=patient.id, disease_group_id=disease_group.id))
        else:
            context = dict(
                patient=patient,
                patient_data=get_patient_data(patient),
                disease_group=disease_group,
                obj=new_obj,
            )

            return render_template(self.get_template_name(), **context)

    def get_template_name(self):
        return 'patient/genetics.html'


class GeneticsEditView(PatientDataEditView):
    disease_group = True
    create = True

    def __init__(self):
        super(GeneticsEditView, self).__init__(
            GeneticsDetailService(current_user),
        )

    def saved(self, patient, obj, disease_group):
        return redirect(url_for('genetics.view_genetics', patient_id=patient.id, disease_group_id=disease_group.id))

    def get_template_name(self):
        return 'patient/edit_genetics.html'


bp.add_url_rule('/<int:disease_group_id>/', view_func=GeneticsDetailView.as_view('view_genetics'))
bp.add_url_rule('/<int:disease_group_id>/edit/', view_func=GeneticsEditView.as_view('edit_genetics'))