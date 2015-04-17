from flask import Flask
from flask_login import LoginManager

from radar.database import db_session, configure_engine
from radar.form_builders import RadarFormBuilder
from radar.medications.views import app as medications_app
from radar.models import User
from radar.views import DemographicsView, LoginView, IndexView, LogoutView, DiseaseGroupView, UnitView
from radar.patients.views import PatientListView
from radar.views import DiseaseGroupsView, UnitsView


app = Flask(__name__)

# TODO load from config file
app.secret_key = 't\xd1\x91\xe5}\xe6\x02\xea\x8c\xecG\xdb}\x0e\xd3Sb$\x9a\xdeW\x15\x01\xc3'

# Configure the database engine
configure_engine('postgresql://postgres:password@localhost:5432/radar')

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

@app.context_processor
def inject_form_builder():
    return dict(form_builder=RadarFormBuilder)

app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/login/', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout/', view_func=LogoutView.as_view('logout'))
app.add_url_rule('/disease-groups/', view_func=DiseaseGroupsView.as_view('disease_groups'))
app.add_url_rule('/disease-groups/<int:disease_group_id>/', view_func=DiseaseGroupView.as_view('disease_group'))
app.add_url_rule('/units/', view_func=UnitsView.as_view('units'))
app.add_url_rule('/units/<int:unit_id>/', view_func=UnitView.as_view('unit'))
app.add_url_rule('/patients/', view_func=PatientListView.as_view('patients'))
app.add_url_rule('/patients/<int:patient_id>/', view_func=DemographicsView.as_view('demographics'))

app.register_blueprint(medications_app, url_prefix='/patients/<int:patient_id>/medications')

if __name__ == '__main__':
    app.run(debug=True)