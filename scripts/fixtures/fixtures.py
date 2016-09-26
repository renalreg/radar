import click

from radar.app import Radar
from radar.database import db

from radar_fixtures import create_data, create_patients, create_users, create_bot_user


def do_drop():
    # Reflect will discover tables that aren't mapped - useful when switching branches
    db.reflect()
    db.drop_all()


def do_create():
    db.create_all()


@click.group()
def cli():
    pass


@cli.command()
@click.pass_context
def drop():
    do_drop()
    db.session.commit()


@cli.command()
def create():
    do_create()
    db.session.commit()


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
