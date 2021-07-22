from datetime import datetime
import os.path
import random

from alembic import command
from alembic.config import Config

from radar.database import no_autoflush
from radar.fixtures.consultants import create_consultants
from radar.fixtures.diagnoses import create_diagnoses
from radar.fixtures.forms import create_forms
from radar.fixtures.groups import create_groups
from radar.fixtures.patients import create_ethnicities, create_patients
from radar.fixtures.posts import create_posts
from radar.fixtures.users import create_bot_user, create_users, DEFAULT_PASSWORD
from radar.fixtures.utils import add
from radar.models.consents import Consent, CONSENT_TYPE


def create_consent():
    consent = Consent()
    consent.code = 'v1'
    consent.label = 'Default consent'
    consent.from_date = datetime(2016, 1, 1, 0, 0, 0)
    consent.consent_type = CONSENT_TYPE.FORM
    consent.weight = 100
    add(consent)


@no_autoflush
def create_data(patients=5, password=DEFAULT_PASSWORD):
    # Always generate the same "random" data
    random.seed(0)

    create_bot_user(password)
    create_consent()
    create_diagnoses()
    create_forms()
    create_groups()
    create_consultants()
    create_posts(10)
    create_users(password)
    create_ethnicities()
    create_patients(patients)
    path = os.path.dirname(__file__)
    cfg = Config(os.path.abspath(os.path.join(path, '../../alembic.ini')))
    command.stamp(cfg, 'head')
