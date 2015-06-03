from flask import request, flash, render_template
from flask.views import View
from flask_login import current_user
from flask import abort

from radar.lib.database import db
from radar.web.forms.core import DeleteForm
from radar.models.disease_groups import DiseaseGroup
from radar.models.patients import Patient


class ListService(object):
    def __init__(self, user):
        self.user = user

    def get_objects(self, patient, *args, **kwargs):
        raise NotImplementedError

    def get_context(self):
        return {}


class DetailService(object):
    def __init__(self, user):
        self.user = user

    def get_object(self, patient, *args, **kwargs):
        raise NotImplementedError

    def new_object(self, patient, *args):
        raise NotImplementedError

    def get_form(self, obj):
        raise NotImplementedError

    def get_context(self):
        return {}

    def validate(self, form, obj):
        return True


class PatientDataDetailView(View):
    methods = ['GET']
    disease_group = False

    def __init__(self, detail_service):
        self.detail_service = detail_service

    def get_template_name(self):
        raise NotImplementedError

    def not_found(self, patient, *args):
        abort(404)

    def dispatch_request(self, patient_id, **kwargs):
        patient = Patient.query.get_or_404(patient_id)

        if not patient.can_view(current_user):
            abort(403)

        context = dict(
            patient=patient,
            patient_data=get_patient_data(patient),
        )

        args = []

        # TODO permissions
        if self.disease_group:
            disease_group_id = kwargs.pop('disease_group_id')
            disease_group = DiseaseGroup.query.get_or_404(disease_group_id)
            args.append(disease_group)
            context['disease_group'] = disease_group

        obj = self.detail_service.get_object(patient, *args, **kwargs)

        if obj is None:
            return self.not_found(patient, *args)

        context['object'] = obj

        if not obj.can_view(current_user):
            abort(403)

        context.update(self.detail_service.get_context())

        return render_template(self.get_template_name(), **context)


class PatientDataAddView(View):
    methods = ['GET', 'POST']
    disease_group = False

    def __init__(self, detail_service):
        self.detail_service = detail_service

    def saved(self, patient, obj, *args):
        raise NotImplementedError

    def get_template_name(self):
        raise NotImplementedError

    def get_form(self, obj):
        return self.detail_service.get_form(obj)

    def get_context(self):
        return {}

    def dispatch_request(self, patient_id, **kwargs):
        patient = Patient.query.get_or_404(patient_id)

        if not patient.can_view(current_user):
            abort(403)

        context = dict(
            patient=patient,
            patient_data=get_patient_data(patient)
        )

        args = []

        # TODO permissions
        if self.disease_group:
            disease_group_id = kwargs.pop('disease_group_id')
            disease_group = DiseaseGroup.query.get(disease_group_id)
            args.append(disease_group)
            context['disease_group'] = disease_group

        obj = self.detail_service.new_object(patient, *args)

        if not obj.can_edit(current_user):
            abort(403)

        form = self.get_form(obj)

        if form and form.validate_on_submit():
            form.populate_obj(obj)

            if self.detail_service.validate(form, obj):
                db.session.add(obj)
                db.session.commit()
                flash('Saved.', 'success')
                return self.saved(patient, obj, *args)

        context.update(dict(
            form=form,
            object=obj
        ))
        context.update(self.get_context())
        context.update(self.detail_service.get_context())

        return render_template(self.get_template_name(), **context)


class PatientDataEditView(View):
    methods = ['GET', 'POST']
    disease_group = False
    create = False

    def __init__(self, detail_service):
        self.detail_service = detail_service

    def get_template_name(self):
        raise NotImplementedError

    def saved(self, patient, obj, *args):
        raise NotImplementedError

    def not_found(self, patient, *args):
        _ = self, patient, args  # not used
        abort(404)

    def dispatch_request(self, patient_id, **kwargs):
        patient = Patient.query.get_or_404(patient_id)

        if not patient.can_view(current_user):
            abort(403)

        context = dict(
            patient=patient,
            patient_data=get_patient_data(patient),
        )

        args = []

        # TODO permissions
        if self.disease_group:
            disease_group_id = kwargs.pop('disease_group_id')
            disease_group = DiseaseGroup.query.get_or_404(disease_group_id)
            args.append(disease_group)
            context['disease_group'] = disease_group

        obj = self.detail_service.get_object(patient, *args, **kwargs)

        if obj is None:
            if self.create:
                obj = self.detail_service.new_object(patient, *args)
            else:
                return self.not_found(patient, *args)

        if not obj.can_edit(current_user):
            abort(403)

        form = self.detail_service.get_form(obj)

        if form.validate_on_submit():
            form.populate_obj(obj)

            if self.detail_service.validate(form, obj):
                db.session.add(obj)
                db.session.commit()
                flash('Saved.', 'success')
                return self.saved(patient, obj, *args)

        context.update(dict(
            object=obj,
            form=form,
        ))
        context.update(self.detail_service.get_context())

        return render_template(self.get_template_name(), **context)


class PatientDataListView(View):
    methods = ['GET']
    disease_group = False

    def __init__(self, list_service):
        self.list_service = list_service

    def get_template_name(self):
        raise NotImplementedError

    def dispatch_request(self, patient_id, **kwargs):
        patient = Patient.query.get_or_404(patient_id)

        if not patient.can_view(current_user):
            abort(403)

        context = dict(
            patient=patient,
            patient_data=get_patient_data(patient),
        )

        args = []

        # TODO permissions
        if self.disease_group:
            disease_group_id = kwargs.pop('disease_group_id')
            disease_group = DiseaseGroup.query.get_or_404(disease_group_id)
            args.append(disease_group)
            context['disease_group'] = disease_group

        objects = self.list_service.get_objects(patient, *args, **kwargs)

        context = dict(
            patient=patient,
            patient_data=get_patient_data(patient),
            objects=objects,
        )
        context.update(self.list_service.get_context())

        return render_template(self.get_template_name(), **context)


class PatientDataListAddView(View):
    methods = ['GET', 'POST']
    disease_group = False
    always_show_list = False

    def __init__(self, list_service, detail_service):
        self.list_service = list_service
        self.detail_service = detail_service

    def saved(self, patient, obj, *args):
        raise NotImplementedError

    def get_template_name(self):
        raise NotImplementedError

    def dispatch_request(self, patient_id, **kwargs):
        patient = Patient.query.get_or_404(patient_id)

        if not patient.can_view(current_user):
            abort(403)

        context = dict(
            patient=patient,
            patient_data=get_patient_data(patient)
        )

        args = []

        # TODO permissions
        if self.disease_group:
            disease_group_id = kwargs.pop('disease_group_id')
            disease_group = DiseaseGroup.query.get(disease_group_id)
            args.append(disease_group)
            context['disease_group'] = disease_group

        objects = self.list_service.get_objects(patient, *args)

        if patient.can_edit(current_user):
            obj = self.detail_service.new_object(patient, *args)
            form = self.detail_service.get_form(obj)
        elif self.always_show_list:
            obj = None
            form = None
        else:
            abort(403)

        if request.method == 'POST':
            if obj is None or not obj.can_edit(current_user):
                abort(403)

            if form.validate():
                form.populate_obj(obj)

                if self.detail_service.validate(form, obj):
                    db.session.add(obj)
                    db.session.commit()
                    flash('Saved.', 'success')
                    return self.saved(patient, obj, *args)

        context.update(dict(
            form=form,
            objects=objects,
            object=obj
        ))
        context.update(self.list_service.get_context())
        context.update(self.detail_service.get_context())

        return render_template(self.get_template_name(), **context)


class PatientDataListDetailView(View):
    methods = ['GET', 'POST']
    disease_group = False

    def __init__(self, list_service, detail_service):
        self.list_service = list_service
        self.detail_service = detail_service

    def get_template_name(self):
        raise NotImplementedError

    def not_found(self, patient, *args):
        _ = self, patient, args  # not used
        abort(404)

    def dispatch_request(self, patient_id, **kwargs):
        patient = Patient.query.get_or_404(patient_id)

        if not patient.can_view(current_user):
            abort(403)

        context = dict(
            patient=patient,
            patient_data=get_patient_data(patient)
        )

        args = []

        # TODO permissions
        if self.disease_group:
            disease_group_id = kwargs.pop('disease_group_id')
            disease_group = DiseaseGroup.query.get(disease_group_id)
            args.append(disease_group)
            context['disease_group'] = disease_group

        objects = self.list_service.get_objects(patient, *args)

        obj = self.detail_service.get_object(patient, *args, **kwargs)

        if obj is None:
            return self.not_found(patient, *args)

        if not obj.can_view(current_user):
            abort(403)

        context.update(dict(
            objects=objects,
            object=obj,
        ))
        context.update(self.list_service.get_context())
        context.update(self.detail_service.get_context())

        return render_template(self.get_template_name(), **context)


class PatientDataListEditView(View):
    methods = ['GET', 'POST']
    disease_group = False

    def __init__(self, list_service, detail_service):
        self.list_service = list_service
        self.detail_service = detail_service

    def saved(self, patient, obj, *args):
        raise NotImplementedError

    def get_template_name(self):
        raise NotImplementedError

    def not_found(self, patient, *args):
        _ = self, patient, args  # not used
        abort(404)

    def dispatch_request(self, patient_id, **kwargs):
        patient = Patient.query.get_or_404(patient_id)

        if not patient.can_view(current_user):
            abort(403)

        context = dict(
            patient=patient,
            patient_data=get_patient_data(patient)
        )

        args = []

        # TODO permissions
        if self.disease_group:
            disease_group_id = kwargs.pop('disease_group_id')
            disease_group = DiseaseGroup.query.get(disease_group_id)
            args.append(disease_group)
            context['disease_group'] = disease_group

        objects = self.list_service.get_objects(patient, *args)

        obj = self.detail_service.get_object(patient, *args, **kwargs)

        if obj is None:
            return self.not_found(patient, *args)

        if not obj.can_edit(current_user):
            abort(403)

        form = self.detail_service.get_form(obj)

        if form.validate_on_submit():
            form.populate_obj(obj)

            if self.detail_service.validate(form, obj):
                db.session.add(obj)
                db.session.commit()
                flash('Saved.', 'success')
                return self.saved(patient, obj, *args)

        context.update(dict(
            objects=objects,
            object=obj,
            form=form,
        ))
        context.update(self.list_service.get_context())
        context.update(self.detail_service.get_context())

        return render_template(self.get_template_name(), **context)


class PatientDataDeleteView(View):
    methods = ['POST']
    disease_group = False

    def __init__(self, detail_service):
        self.detail_service = detail_service

    def deleted(self, patient, *args):
        raise NotImplementedError

    def not_found(self, patient, *args):
        _ = self, patient, args  # not used
        abort(404)

    def dispatch_request(self, patient_id, **kwargs):
        patient = Patient.query.get_or_404(patient_id)

        if not patient.can_edit(current_user):
            abort(403)

        args = []

        # TODO permissions
        if self.disease_group:
            disease_group_id = kwargs.pop('disease_group_id')
            disease_group = DiseaseGroup.query.get_or_404(disease_group_id)
            args.append(disease_group)

        obj = self.detail_service.get_object(patient, *args, **kwargs)

        if obj is None:
            return self.not_found(*args)

        form = DeleteForm()

        if not obj.can_edit(current_user) or not form.validate_on_submit():
            abort(403)

        db.session.delete(obj)
        db.session.commit()

        return self.deleted(patient, *args)


def get_patient_data(patient):
    units = sorted(patient.filter_units_for_user(current_user), key=lambda x: x.unit.name.lower())
    disease_groups = sorted(patient.filter_disease_groups_for_user(current_user), key=lambda x: x.disease_group.name.lower())

    return dict(
        units=units,
        disease_groups=disease_groups,
    )
