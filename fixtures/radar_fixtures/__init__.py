import random

from radar.database import db
from radar_fixtures.users import DEFAULT_PASSWORD
from radar_fixtures.organisations import create_organisations
from radar_fixtures.data_sources import create_data_sources
from radar_fixtures.results import create_result_specs, create_result_group_specs
from radar_fixtures.cohorts import create_cohorts
from radar_fixtures.diagnoses import create_cohort_diagnoses
from radar_fixtures.comorbidities import create_disorders
from radar_fixtures.users import create_users, create_bot_user
from radar_fixtures.consultants import create_consultants
from radar_fixtures.posts import create_posts
from radar_fixtures.patients import create_patients

__version__ = '0.1.0'


def create_data(patients=5, users=10, password=DEFAULT_PASSWORD):
    # Always generate the same "random" data
    random.seed(0)

    with db.session.no_autoflush:
        create_bot_user(password)
        create_organisations()
        create_data_sources()
        create_cohorts()
        create_cohort_diagnoses()
        create_result_specs()
        create_result_group_specs()
        create_disorders()
        create_consultants()
        create_posts(10)
        create_users(users, password)
        create_patients(patients)
