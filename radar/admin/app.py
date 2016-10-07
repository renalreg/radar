from flask import request, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView as BaseAdminIndexView
from flask_admin import expose, helpers
from wtforms import form, fields, validators

from radar.app import Radar
from radar.auth.sessions import login, logout, current_user, UsernameLoginError, PasswordLoginError, DisabledLoginError
from radar.database import db
from radar.models.diagnoses import Diagnosis
from radar.models.groups import Group
from radar.models.medications import Drug, DrugGroup
from radar.models.results import Observation
from radar.models.consultants import Consultant, Specialty


class ConsultantView(ModelView):
    pass


class DiagnosisView(ModelView):
    column_default_sort = 'name'
    column_searchable_list = ['name', 'edta']


class DrugView(ModelView):
    pass


class DrugGroupView(ModelView):
    pass


class GroupView(ModelView):
    pass


class ObservationView(ModelView):
    pass


class SpecialtyView(ModelView):
    pass


class LoginForm(form.Form):
    username = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])


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

        self._template_args['form'] = form

        return super(AdminIndexView, self).index()

    @expose('/logout/')
    def logout(self):
        logout()
        return redirect(url_for('.index'))


def inject_current_user():
    return dict(current_user=current_user)


def create_app():
    app = Radar(template_folder='admin/templates')
    app.context_processor(inject_current_user)

    admin = Admin(app, 'RADAR Admin', index_view=AdminIndexView(url=''), template_mode='bootstrap3', base_template='master.html')
    admin.add_view(ConsultantView(Consultant, db.session))
    admin.add_view(DiagnosisView(Diagnosis, db.session))
    admin.add_view(DrugView(Drug, db.session))
    admin.add_view(DrugGroupView(DrugGroup, db.session))
    admin.add_view(GroupView(Group, db.session))
    admin.add_view(ObservationView(Observation, db.session))
    admin.add_view(SpecialtyView(Specialty, db.session))

    return app
