from flask import request, redirect, url_for
from flask_admin import AdminIndexView as BaseAdminIndexView
from flask_admin import expose, helpers
from flask_admin.contrib.sqla import ModelView as BaseModelView
from flask_admin.contrib.sqla.form import AdminModelConverter as BaseAdminModelConverter
from flask_admin.model.form import converts
from wtforms import fields

from radar.admin.fields import EnumSelectField
from radar.admin.forms import LoginForm
from radar.auth.sessions import login, logout, current_user, UsernameLoginError, PasswordLoginError, DisabledLoginError


class AdminModelConverter(BaseAdminModelConverter):
    @converts('EnumType')
    def convert_enum_type(self, column, field_args, **extra):
        return EnumSelectField(column.type.enum_class, **field_args)

    @converts('EnumToStringType')
    def convert_enum_to_string_type(self, column, field_args, **extra):
        return EnumSelectField(column.type.enum_class, **field_args)


class ModelView(BaseModelView):
    model_form_converter = AdminModelConverter
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_admin


class AdminIndexView(BaseAdminIndexView):
    @expose('/')
    def index(self):
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
    column_default_sort = 'id'
    column_export_list = ['id', 'diagnosis', 'code']


class DrugView(ModelView):
    column_default_sort = 'name'
    column_list = ['name', 'drug_group']
    form_columns = ['name', 'drug_group']
    column_searchable_list = ['name']
    column_export_list = ['id', 'name', 'drug_group']


class DrugGroupView(ModelView):
    column_default_sort = 'name'
    column_list = ['name', 'parent_drug_group']
    column_default_sort = 'name'
    form_columns = ['name', 'parent_drug_group']
    column_searchable_list = ['name']
    column_export_list = ['id', 'name', 'parent_drug_group']


class GroupView(ModelView):
    column_list = ['name', 'type', 'code', 'parent_group']
    column_default_sort = 'name'
    form_columns = ['name', 'short_name', 'type', 'code', 'parent_group', 'instructions']
    column_searchable_list = ['name', 'short_name', 'type', 'code']
    column_export_list = ['id', 'name', 'short_name', 'type', 'code', 'parent_group', 'instructions']
    form_extra_fields = dict(instructions=fields.TextAreaField())


class GroupConsultantView(ModelView):
    column_default_sort = 'id'
    column_export_list = ['id', 'group', 'consultant']


class GroupDiagnosisView(ModelView):
    column_default_sort = 'id'
    column_export_list = ['id', 'group', 'diagnosis', 'weight']


class GroupFormView(ModelView):
    column_default_sort = 'id'
    column_export_list = ['id', 'group', 'form', 'weight']


class GroupObservationView(ModelView):
    column_default_sort = 'id'
    column_export_list = ['id', 'group', 'observation']


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
    column_list = ['name', 'sample_type']
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
