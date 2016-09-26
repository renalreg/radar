import click

from radar.app import Radar
from radar.database import db, do_create, do_drop

from radar_fixtures import create_data, create_patients, create_users, create_bot_user


@click.group()
def cli():
    pass


@cli.command()
@click.option('--patients', default=5)
@click.option('--password', default='password')
def all(patients, password):
    do_drop()
    do_create()
    create_data(patients=patients, password=password)
    db.session.commit()


@cli.command()
@click.option('--patients', default=5)
@click.option('--data/--no-data', default=True)
def patients(patients, data):
    create_patients(patients, data)
    db.session.commit()


@cli.command()
@click.option('--password', default='password')
def users(password):
    create_bot_user(password)
    create_users(password)
    db.session.commit()


if __name__ == '__main__':
    app = Radar()

    with app.app_context():
        cli()
