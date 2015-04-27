from flask import Flask
from flask_login import LoginManager

from radar.database import db_session, init_engine
from radar.diagnoses.views import DiagnosisDetailView
from radar.demographics.views import DemographicsListView, DemographicsDetailViewView
from radar.medications.views import MedicationDetailView, MedicationDeleteView, MedicationListView
from radar.models import User
from radar.users.views import UserListView, UserDetailView, UserUnitsView, UserDiseaseGroupsView
from radar.utils import url_for_page, url_for_per_page, current_order_by, url_for_order_by, current_order_direction
from radar.views import IndexView, DiseaseGroupView, UnitView, AdminView
from radar.patient_list.views import PatientListView, PatientUnitsView, PatientDiseaseGroupsView
from radar.views import DiseaseGroupsView, UnitsView
from radar.authentication.views import LoginView, LogoutView


app = Flask(__name__)

# TODO load from config file
app.secret_key = 't\xd1\x91\xe5}\xe6\x02\xea\x8c\xecG\xdb}\x0e\xd3Sb$\x9a\xdeW\x15\x01\xc3'

# Configure the database engine
init_engine('postgresql://postgres:password@localhost:5432/radar')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# noinspection PyUnusedLocal
@app.teardown_appcontext
def shutdown_session(exception=None):
    # Remove the database session at the end of the request
    db_session.remove()

@app.template_filter('datetime_format')
def datetime_format(dt, datetime_format):
    if dt is None:
        return ''
    else:
        return dt.strftime(datetime_format)

app.jinja_env.globals.update({
    'url_for_page': url_for_page,
    'url_for_per_page': url_for_per_page,
    'url_for_order_by': url_for_order_by,
    'current_order_by': current_order_by,
    'current_order_direction': current_order_direction,
})

app.add_url_rule('/', view_func=IndexView.as_view('index'))

app.add_url_rule('/login/', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout/', view_func=LogoutView.as_view('logout'))

app.add_url_rule('/disease-groups/', view_func=DiseaseGroupsView.as_view('disease_groups'))
app.add_url_rule('/disease-groups/<int:disease_group_id>/', view_func=DiseaseGroupView.as_view('disease_group'))

app.add_url_rule('/units/', view_func=UnitsView.as_view('units'))
app.add_url_rule('/units/<int:unit_id>/', view_func=UnitView.as_view('unit'))

app.add_url_rule('/patients/', view_func=PatientListView.as_view('patients'))
app.add_url_rule('/patients/<int:patient_id>/', view_func=DemographicsListView.as_view('patient'))
app.add_url_rule('/patients/<int:patient_id>/', view_func=DemographicsListView.as_view('demographics'))
app.add_url_rule('/patients/<int:patient_id>/edit', view_func=DemographicsDetailViewView.as_view('demographics_update'))
app.add_url_rule('/patients/<int:patient_id>/disease-groups/', view_func=PatientDiseaseGroupsView.as_view('patient_disease_groups'))
app.add_url_rule('/patients/<int:patient_id>/units/', view_func=PatientUnitsView.as_view('patient_units'))
app.add_url_rule('/patients/<int:patient_id>/diagnosis/<int:disease_group_id>/', view_func=DiagnosisDetailView.as_view('diagnosis'))
app.add_url_rule('/patients/<int:patient_id>/medications/', view_func=MedicationListView.as_view('medications'))
app.add_url_rule('/patients/<int:patient_id>/medications/new', view_func=MedicationDetailView.as_view('medication_create'))
app.add_url_rule('/patients/<int:patient_id>/medications/<int:entry_id>/', view_func=MedicationDetailView.as_view('medication_update'))
app.add_url_rule('/patients/<int:patient_id>/medications/<int:entry_id>/', view_func=MedicationDetailView.as_view('medication_detail'))
app.add_url_rule('/patients/<int:patient_id>/medications/<int:entry_id>/', view_func=MedicationDeleteView.as_view('medication_delete'))

app.add_url_rule('/users/', view_func=UserListView.as_view('users'))
app.add_url_rule('/users/<int:user_id>/', view_func=UserDetailView.as_view('user'))
app.add_url_rule('/users/<int:user_id>/disease-groups/', view_func=UserUnitsView.as_view('user_disease_groups'))
app.add_url_rule('/users/<int:user_id>/units/', view_func=UserDiseaseGroupsView.as_view('user_units'))

app.add_url_rule('/admin/', view_func=AdminView.as_view('admin'))

if __name__ == '__main__':
    app.run(debug=True)