from sqlalchemy import func

from radar.models.users import User
from radar_fixtures.validation import validate_and_add
from radar.database import db
from radar_fixtures.utils import generate_gender, generate_first_name, generate_last_name
from radar.roles import ROLES
from radar.models.groups import Group, GroupUser, GROUP_TYPE_HOSPITAL, GROUP_TYPE_COHORT

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

    group_user = GroupUser()
    group_user.user = user
    group_user.group = Group.query.filter(Group.code == 'REE01', Group.type == GROUP_TYPE_HOSPITAL).one()
    group_user.role = ROLES.SENIOR_CLINICIAN
    validate_and_add(group_user)


def create_ins_user(password=DEFAULT_PASSWORD):
    user = User()
    user.username = 'ins_demo'
    user.email = 'ins_demo@example.org'
    user.first_name = 'Foo'
    user.last_name = 'Bar'
    user.is_admin = False
    user.password = password
    user = validate_and_add(user, {'allow_weak_passwords': True})

    group_user = GroupUser()
    group_user.user = user
    group_user.group = Group.query.filter(Group.code == 'INS', Group.type == GROUP_TYPE_COHORT).one()
    group_user.role = ROLES.RESEARCHER
    validate_and_add(group_user)


def create_ins_demograhics_user(password=DEFAULT_PASSWORD):
    user = User()
    user.username = 'ins_demographics_demo'
    user.email = 'ins_demographics_demo@example.org'
    user.first_name = 'Foo'
    user.last_name = 'Bar'
    user.is_admin = False
    user.password = password
    user = validate_and_add(user, {'allow_weak_passwords': True})

    group_user = GroupUser()
    group_user.user = user
    group_user.group = Group.query.filter(Group.code == 'INS', Group.type == GROUP_TYPE_COHORT).one()
    group_user.role = ROLES.SENIOR_RESEARCHER
    validate_and_add(group_user)
