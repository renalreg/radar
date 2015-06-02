from flask_script import Manager

from radar.web.app import create_app
from radar.lib.database import db
from radar.lib import fixtures

app = create_app()

manager = Manager(app)


@manager.command
def create_tables():
    db.drop_all()
    db.create_all()


@manager.command
def drop_tables():
    db.drop_all()


@manager.command
def load_data():
    fixtures.create_fixtures()
    db.session.commit()


@manager.command
def reload_data():
    create_tables()
    load_data()


if __name__ == '__main__':
    manager.run()
