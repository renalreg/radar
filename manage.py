from flask_script import Manager

from radar.web.app import create_app
from radar.lib.database import db
from radar.lib.data import dev, create_initial_data

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
def initdb():
    db.create_all()
    create_initial_data()


@manager.command
def devdb():
    db.drop_all()
    db.create_all()
    dev.create_data()
    db.session.commit()


if __name__ == '__main__':
    manager.run()
