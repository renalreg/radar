from flask import Flask
from flask_login import LoginManager, current_user

from radar.users.services import load_user
from radar.disease_groups.services import get_disease_groups_for_user
from radar.ordering import url_for_order_by
from radar.pagination import url_for_per_page, url_for_page
from radar.template_filters import datetime_format
from radar.units.services import get_units_for_user
from radar.views import bp as radar_bp
from radar.diagnosis.views import bp as diagnosis_bp
from radar.disease_groups.views import bp as disease_groups_bp
from radar.medications.views import bp as medications_bp
from radar.patients.views import bp as patients_bp
from radar.units.views import bp as units_bp
from radar.users.views import bp as users_bp, require_login
from radar.database import db


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    app.register_blueprint(radar_bp)
    app.register_blueprint(disease_groups_bp, url_prefix='/disease-groups')
    app.register_blueprint(units_bp, url_prefix='/units')
    app.register_blueprint(users_bp)
    app.register_blueprint(patients_bp, url_prefix='/patients')

    patient_blueprints = [
        (medications_bp, '/medications'),
        (diagnosis_bp, '/diagnoses'),
    ]

    patient_base = '/patients/<int:patient_id>'

    for bp, url_prefix in patient_blueprints:
        app.register_blueprint(bp, url_prefix=patient_base + url_prefix)

    login_manager.user_loader(load_user)
    login_manager.login_view = 'users.login'

    app.before_request(require_login)

    app.add_template_filter(datetime_format)

    @app.context_processor
    def inject_navigation():
        navigation = dict()

        if current_user.is_authenticated():
            navigation['units'] = get_units_for_user(current_user)
            navigation['disease_groups'] = get_disease_groups_for_user(current_user)

        return dict(navigation=navigation)

    app.add_template_global(url_for_order_by)
    app.add_template_global(url_for_page)
    app.add_template_global(url_for_per_page)

    return app