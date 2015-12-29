from sqlalchemy import func

from radar.models.users import User
from radar.fixtures.validation import validate_and_add
from radar.database import db

DEFAULT_PASSWORD = 'password'


def create_users(password=DEFAULT_PASSWORD):
    create_bot_user(password)
    create_admin_user(password)


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
