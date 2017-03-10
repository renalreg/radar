import random

from radar.database import no_autoflush
from radar.fixtures.consultants import create_consultants
from radar.fixtures.diagnoses import create_diagnoses
from radar.fixtures.forms import create_forms
from radar.fixtures.groups import create_groups
from radar.fixtures.patients import create_patients
from radar.fixtures.posts import create_posts
from radar.fixtures.users import create_bot_user, create_users, DEFAULT_PASSWORD


@no_autoflush
def create_data(patients=5, password=DEFAULT_PASSWORD):
    # Always generate the same "random" data
    random.seed(0)

    create_bot_user(password)
    create_diagnoses()
    create_forms()
    create_groups()
    create_consultants()
    create_posts(10)
    create_users(password)
    create_patients(patients)
