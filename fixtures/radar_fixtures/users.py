from sqlalchemy import func

from radar.models.users import User
from radar_fixtures.validation import validate_and_add
from radar.database import db
from radar_fixtures.utils import generate_gender, generate_first_name, generate_last_name
from radar.models.organisations import OrganisationUser, Organisation
from radar.roles import ORGANISATION_ROLES, COHORT_ROLES
from radar.models.cohorts import CohortUser, Cohort

DEFAULT_PASSWORD = 'password'


def create_users(n, password=DEFAULT_PASSWORD):
    create_admin_user(password)
    create_southmead_user(password)
    create_ins_user(password)
    create_ins_demograhics_user(password)

    for x in range(n):
        username = 'user%d' % (x + 1)
        user = User()
        user.first_name = generate_first_name(generate_gender()).capitalize()
        user.last_name = generate_last_name().capitalize()
        user.username = username
        user.email = '%s@example.org' % username
        user.password = password
        user.is_admin = True
        validate_and_add(user, {'allow_weak_passwords': True})


def create_bot_user(password=DEFAULT_PASSWORD):
    bot = User()
    bot.username = 'bot'
    bot.email = 'bot@example.org'
    bot.is_admin = True
    bot.is_bot = True
    bot.password = password
    bot.created_user = bot
    bot.modified_user = bot
    bot.created_date = func.now()
    bot.modified_date = func.now()
    db.session.add(bot)
    db.session.flush()


def create_admin_user(password=DEFAULT_PASSWORD):
    user = User()
    user.username = 'admin'
    user.email = 'admin@example.org'
    user.first_name = 'Foo'
    user.last_name = 'Bar'
    user.is_admin = True
    user.password = password
    validate_and_add(user, {'allow_weak_passwords': True})


def create_southmead_user(password=DEFAULT_PASSWORD):
    user = User()
    user.username = 'southmead_demo'
    user.email = 'southmead_demo@example.org'
    user.first_name = 'Foo'
    user.last_name = 'Bar'
    user.is_admin = False
    user.password = password
    user = validate_and_add(user, {'allow_weak_passwords': True})

    organisation_user = OrganisationUser()
    organisation_user.user = user
    organisation_user.organisation = Organisation.query.filter(Organisation.code == 'REE01').one()
    organisation_user.role = ORGANISATION_ROLES.SENIOR_CLINICIAN
    validate_and_add(organisation_user)


def create_ins_user(password=DEFAULT_PASSWORD):
    user = User()
    user.username = 'ins_demo'
    user.email = 'ins_demo@example.org'
    user.first_name = 'Foo'
    user.last_name = 'Bar'
    user.is_admin = False
    user.password = password
    user = validate_and_add(user, {'allow_weak_passwords': True})

    cohort_user = CohortUser()
    cohort_user.user = user
    cohort_user.cohort = Cohort.query.filter(Cohort.code == 'INS').one()
    cohort_user.role = COHORT_ROLES.RESEARCHER
    validate_and_add(cohort_user)


def create_ins_demograhics_user(password=DEFAULT_PASSWORD):
    user = User()
    user.username = 'ins_demographics_demo'
    user.email = 'ins_demographics_demo@example.org'
    user.first_name = 'Foo'
    user.last_name = 'Bar'
    user.is_admin = False
    user.password = password
    user = validate_and_add(user, {'allow_weak_passwords': True})

    cohort_user = CohortUser()
    cohort_user.user = user
    cohort_user.cohort = Cohort.query.filter(Cohort.code == 'INS').one()
    cohort_user.role = COHORT_ROLES.SENIOR_RESEARCHER
    validate_and_add(cohort_user)
