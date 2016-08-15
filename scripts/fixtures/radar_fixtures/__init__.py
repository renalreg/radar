import random

from radar.database import no_autoflush

from radar_fixtures.users import DEFAULT_PASSWORD
from radar_fixtures.groups import create_groups
from radar_fixtures.diagnoses import create_diagnoses
from radar_fixtures.users import create_users, create_bot_user
from radar_fixtures.consultants import create_consultants
from radar_fixtures.posts import create_posts
from radar_fixtures.patients import create_patients


@no_autoflush
def create_data(patients=5, password=DEFAULT_PASSWORD):
    # Always generate the same "random" data
    random.seed(0)

    create_bot_user(password)
    create_groups()
    create_diagnoses()
    create_consultants()
    create_posts(10)
    create_users(password)
    create_patients(patients)
