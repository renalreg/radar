#!/usr/bin/env python

import click

from radar.app import Radar
from radar.database import db, do_create, do_drop
from radar.fixtures import create_bot_user, create_data, create_patients, create_users
from radar.fixtures.users import create_user


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


@cli.command()
@click.argument('username')
@click.option('--password', default='password')
def user(username, password):
    create_user(username, password)
    db.session.commit()


def main():
    app = Radar()

    with app.app_context():
        cli()


if __name__ == '__main__':
    main()
