from flask_script import Manager

from radar.app import create_app
from radar.lib.database import db
from radar.models.users import User
from radar.data import fixtures

app = create_app('settings.py')

manager = Manager(app)


@manager.command
def create_tables():
    db.drop_all()
    db.create_all()


@manager.command
def drop_tables():
    db.drop_all()


@manager.command
def create_admin():
    user = User()
    user.username = 'admin'
    user.email = 'admin@example.org'
    user.set_password('password')
    user.is_admin = True
    db.session.add(user)
    db.session.commit()


@manager.command
def create_fixtures():
    fixtures.create_fixtures()
    db.session.commit()


if __name__ == '__main__':
    manager.run()