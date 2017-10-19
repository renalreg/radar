"""Admin views."""
import glob
import io
import os

from flask import redirect, request, send_file, url_for
from flask_admin import AdminIndexView as BaseAdminIndexView
from flask_admin import BaseView, expose, helpers
from flask_admin.contrib.sqla import ModelView as BaseModelView
from flask_admin.contrib.sqla.form import AdminModelConverter as BaseAdminModelConverter
from flask_admin.model.form import converts
from sqlalchemy import func
from wtforms import fields

from radar.admin.fields import EnumSelectField
from radar.admin.forms import LoginForm
from radar.auth.sessions import (
    current_user,
    DisabledLoginError,
    login,
    logout,
    PasswordLoginError,
    UsernameLoginError,
)
from radar.config import config
from radar.models.groups import Group, GROUP_TYPE


class AdminModelConverter(BaseAdminModelConverter):
    @converts('EnumType')
    def convert_enum_type(self, column, field_args, **extra):
        """Converter for the SQLAlchemy EnumType."""
        return EnumSelectField(column.type.enum_class, **field_args)

    @converts('EnumToStringType')
    def convert_enum_to_string_type(self, column, field_args, **extra):
        """Converter for the SQLAlchemy EnumToStringType."""
        return EnumSelectField(column.type.enum_class, **field_args)


class ModelView(BaseModelView):
    model_form_converter = AdminModelConverter
    can_export = True  # Enable CSV exports

    def is_accessible(self):
        # User needs to be logged in and a super admin to use this view
        return current_user.is_authenticated() and current_user.is_admin


class AdminIndexView(BaseAdminIndexView):
    @expose('/')
    def index(self):
        # If the user isn't logged in, redirect them to the login page
        if not current_user.is_authenticated():
            return redirect(url_for('.login'))

        return super(AdminIndexView, self).index()

    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        form = LoginForm(request.form)

        if helpers.validate_form_on_submit(form):
            username = form.username.data
            password = form.password.data

            try:
                user, _ = login(username, password)
            except (UsernameLoginError, PasswordLoginError):
                form.username.errors.append('Incorrect username or password.')
            except DisabledLoginError:
                form.username.errors.append('Account disabled, please contact support.')

            # Logged in successfully
            if current_user.is_authenticated():
                return redirect(url_for('.index'))

        return self.render('admin/login.html', form=form)

    @expose('/logout/')
    def logout(self):
        logout()
        return redirect(url_for('.index'))


class CodeView(ModelView):
    column_default_sort = 'id'
    form_columns = ['system', 'code', 'display']
    column_searchable_list = ['system', 'code', 'display']
    column_export_list = ['id', 'system', 'code', 'display']


class ConsultantView(ModelView):
    column_default_sort = 'last_name'
    column_list = ['first_name', 'last_name', 'specialty', 'email']
    form_columns = ['first_name', 'last_name', 'specialty', 'email', 'telephone_number', 'gmc_number']
    column_labels = dict(gmc_number='GMC Number')
    column_searchable_list = ['first_name', 'last_name', 'email', 'telephone_number', 'gmc_number']
    column_export_list = ['id', 'first_name', 'last_name', 'specialty', 'email', 'telephone_number', 'gmc_number']


class DiagnosisView(ModelView):
    column_default_sort = 'name'
    column_searchable_list = ['name']
    column_export_list = ['id', 'name']


class DiagnosisCodeView(ModelView):
    column_default_sort = 'diagnosis.name'
    column_auto_select_related = True
    column_searchable_list = ['diagnosis.name']
    column_export_list = ['id', 'diagnosis', 'code']


class DrugView(ModelView):
    column_default_sort = 'name'
    column_list = ['name', 'drug_group']
    form_columns = ['name', 'drug_group']
    column_searchable_list = ['name']
    column_export_list = ['id', 'name', 'drug_group']


class CountryView(ModelView):
    column_list = ['code', 'label']
    form_columns = ['code', 'label']
    column_searchable_list = ['code', 'label']


class CountryEthnicityView(ModelView):
    pass


class CountryNationalityView(ModelView):
    pass


class EthnicityView(ModelView):
    column_list = ['code', 'label']
    form_columns = ['code', 'label']


class NationalityView(ModelView):
    column_list = ['label']
    form_columns = ['label']


class DrugGroupView(ModelView):
    column_default_sort = 'name'
    column_list = ['name', 'parent_drug_group']
    column_default_sort = 'name'
    form_columns = ['name', 'parent_drug_group']
    column_searchable_list = ['name']
    column_export_list = ['id', 'name', 'parent_drug_group']


class GroupView(ModelView):
    column_list = ['name', 'type', 'code', 'country']
    column_default_sort = 'name'
    form_columns = [
        'name',
        'short_name',
        'type',
        'code',
        'country',
        'is_recruitment_number_group',
        'instructions',
    ]
    column_searchable_list = ['name', 'short_name', 'type', 'code', 'country.label']
    column_export_list = ['id', 'name', 'short_name', 'type', 'code', 'country', 'instructions']
    form_extra_fields = dict(instructions=fields.TextAreaField())

    def create_form(self):
        form = super(GroupView, self).create_form()
        form.type.iter_choices = self._filtered_parent
        return form

    def edit_form(self, obj):
        form = super(GroupView, self).edit_form(obj)
        form.type.iter_choices = self._filtered_parent
        return form

    def _filtered_parent(self):
        """Don't show COHORTS and HOSPITALS in select field."""
        for enum in GROUP_TYPE:
            if enum.name in ('COHORT', 'HOSPITAL'):
                continue
            yield enum.name, enum.value, enum

    def on_model_change(self, form, model, is_created):
        if model.type != GROUP_TYPE.OTHER and model.is_recruitment_number_group:
            model.is_recruitment_number_group = False
        super(GroupView, self).on_model_change(form, model, is_created)

    def get_query(self):
        query = super(GroupView, self).get_query()
        query = query.filter(self.model.type != GROUP_TYPE.HOSPITAL)
        query = query.filter(self.model.type != GROUP_TYPE.COHORT)
        return query

    def get_count_query(self):
        query = self.session.query(func.count('*')).select_from(self.model)
        query = query.filter(self.model.type != GROUP_TYPE.HOSPITAL)
        query = query.filter(self.model.type != GROUP_TYPE.COHORT)
        return query


class HospitalView(ModelView):
    column_list = ['name', 'code', 'is_transplant_centre', 'country']
    column_default_sort = 'name'
    column_searchable_list = ['name', 'short_name', 'code', 'country_code', 'country.label']
    form_columns = ['name', 'short_name', 'code', 'country', 'instructions', 'is_transplant_centre']

    def on_model_change(self, form, model, is_created):
        model.type = GROUP_TYPE.HOSPITAL
        super(HospitalView, self).on_model_change(form, model, is_created)

    def get_query(self):
        return super(ModelView, self).get_query().filter(self.model.type == GROUP_TYPE.HOSPITAL)

    def get_count_query(self):
        query = self.session.query(func.count('*')).select_from(self.model)
        query = query.filter(self.model.type == GROUP_TYPE.HOSPITAL)
        return query


class CohortView(ModelView):
    column_list = ['name', 'code', 'parent_group']
    column_default_sort = 'name'
    column_searchable_list = ['name', 'short_name', 'code']
    form_columns = ['name', 'short_name', 'code', 'parent_group', 'instructions']
    form_extra_fields = dict(instructions=fields.TextAreaField())

    def create_form(self):
        form = super(CohortView, self).create_form()
        query = form.parent_group.query_factory()
        form.parent_group.query = query.filter(Group.type == GROUP_TYPE.SYSTEM)
        return form

    def edit_form(self, obj):
        form = super(CohortView, self).edit_form(obj)
        query = form.parent_group.query_factory()
        form.parent_group.query = query.filter(Group.type == GROUP_TYPE.SYSTEM)
        return form

    def on_model_change(self, form, model, is_created):
        model.type = GROUP_TYPE.COHORT
        super(CohortView, self).on_model_change(form, model, is_created)

    def get_query(self):
        return super(CohortView, self).get_query().filter(self.model.type == GROUP_TYPE.COHORT)

    def get_count_query(self):
        query = self.session.query(func.count('*')).select_from(self.model)
        query = query.filter(self.model.type == GROUP_TYPE.COHORT)
        return query


class GroupConsultantView(ModelView):
    column_default_sort = 'id'
    column_export_list = ['id', 'group', 'consultant']


class GroupDiagnosisView(ModelView):
    column_default_sort = 'group.name'
    column_auto_select_related = True
    column_searchable_list = ['group.name', 'diagnosis.name']
    column_export_list = ['id', 'group', 'diagnosis', 'weight']


class GroupFormView(ModelView):
    column_default_sort = 'id'
    column_export_list = ['id', 'group', 'form', 'weight']


class GroupObservationView(ModelView):
    column_default_sort = 'id'
    column_export_list = ['id', 'group', 'observation', 'weight']


class GroupPageView(ModelView):
    column_default_sort = 'id'
    column_export_list = ['id', 'group', 'page', 'weight']


class GroupQuestionnaireView(ModelView):
    column_default_sort = 'id'
    column_export_list = ['id', 'group', 'form', 'weight']


class FormView(ModelView):
    column_default_sort = 'name'
    column_list = ['name', 'slug']
    form_columns = ['name', 'slug', 'data']
    column_searchable_list = ['name', 'slug', 'data']
    column_export_list = ['id', 'name', 'slug', 'data']


class ObservationView(ModelView):
    column_default_sort = 'name'
    column_list = ['name', 'short_name', 'sample_type']
    form_columns = [
        'name', 'short_name', 'value_type',
        'sample_type', 'pv_code', 'min_value',
        'max_value', 'min_length', 'max_length',
        'units', 'options',
    ]
    column_labels = dict(pv_code='PV Code')
    column_searchable_list = ['name', 'short_name', 'value_type', 'sample_type', 'pv_code', 'options', 'units']
    column_export_list = [
        'id', 'name', 'short_name',
        'value_type', 'sample_type', 'pv_code',
        'min_value' 'max_value', 'min_length',
        'max_length', 'units', 'options',
    ]


class SpecialtyView(ModelView):
    column_default_sort = 'name'
    column_searchable_list = ['name']
    column_export_list = ['id', 'name']


class ExportView(BaseView):
    """Basic view to expose export functionality."""

    @expose('/', methods=['GET'])
    def index(self):
        """Default page listing files in the directory."""

        files = glob.glob(os.path.join(config.get('EXPORT_PATH'), '*.xlsx'))
        files = [os.path.split(path)[1] for path in files]
        return self.render('admin/export.html', files=files)

    @expose('/<string:param>', methods=['GET'])
    def serve_file(self, param):
        """Serve back requested file."""
        requested_file = io.open(os.path.join(config.get('EXPORT_PATH'), param), 'rb')
        return send_file(requested_file, as_attachment=True, attachment_filename=param)


class ConsentView(ModelView):
    column_list = ['code', 'label', 'paediatric', 'from_date', 'retired']
    form_columns = ['code', 'label', 'paediatric', 'from_date', 'link_url', 'retired']
