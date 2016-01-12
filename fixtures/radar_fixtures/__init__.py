import random

from radar.database import db
from radar_fixtures.users import DEFAULT_PASSWORD
from radar_fixtures.groups import create_groups
from radar_fixtures.diagnoses import create_group_diagnoses
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
        create_groups()
        create_group_diagnoses()
        create_disorders()
        create_consultants()
        create_posts(10)
        create_users(users, password)
        create_patients(patients)
