from flask import Flask

from radar.database import db_session, configure_engine
from radar.medications.views import app as medications_app
from radar.views import PatientsView, PatientView


app = Flask(__name__)

# Configure the database engine
configure_engine('postgresql://postgres:password@localhost:5432/radar')

# noinspection PyUnusedLocal
@app.teardown_appcontext
def shutdown_session(exception=None):
    # Remove the database session at the end of the request
    db_session.remove()

@app.template_filter('date_format')
def date_format(dt, format):
    if dt is None:
        return ''
    else:
        return dt.strftime(format)

app.add_url_rule('/patients/', view_func=PatientsView.as_view('patients'))
app.add_url_rule('/patients/<int:patient_id>/', view_func=PatientView.as_view('patient'))

app.register_blueprint(medications_app, url_prefix='/patients/<int:patient_id>/medications')

if __name__ == '__main__':
    app.run(debug=True)