from sqlalchemy import or_, func

from radar.models.users import User
from radar_fixtures.validation import validate_and_add
from radar_fixtures.utils import generate_gender, generate_first_name, generate_last_name
from radar.roles import ROLE
from radar.models.groups import Group, GroupUser, GROUP_TYPE
from radar.database import db

DEFAULT_PASSWORD = 'password'


def create_users(password=DEFAULT_PASSWORD):
    create_admin_user(password)
    create_ukrdc_importer_user(password)

    for group in Group.query.filter(or_(Group.type == GROUP_TYPE.COHORT, Group.type == GROUP_TYPE.HOSPITAL)):
        for role in ROLE:
            user = User()
            user.first_name = generate_first_name(generate_gender()).capitalize()
            user.last_name = generate_last_name().capitalize()
            user.username = group.code.lower() + '_' + str(role).lower()
            user.email = '%s@example.org' % user.username
            user.password = password
            validate_and_add(user, {'allow_weak_passwords': True})

            group_user = GroupUser()
            group_user.user = user
            group_user.group = group
            group_user.role = role
            validate_and_add(group_user)


def create_bot_user(password=DEFAULT_PASSWORD):
    bot = User()
    bot.username = 'bot'
    bot.is_admin = True
    bot.is_bot = True
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


def create_ukrdc_importer_user(password=DEFAULT_PASSWORD):
    user = User()
    user.username = 'ukrdc_importer'
    user.is_admin = True
    user.is_bot = True
    validate_and_add(user, {'allow_weak_passwords': True})
