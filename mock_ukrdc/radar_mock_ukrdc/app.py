from flask import Flask

from radar_mock_ukrdc.views import PatientSearchView


def create_app():
    app = Flask(__name__)

    app.config.from_object('radar_mock_ukrdc.default_settings')
    app.config.from_envvar('RADAR_SETTINGS')

    app.add_url_rule('/search', view_func=PatientSearchView.as_view('patient_search'))

    return app
