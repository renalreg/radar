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
@click.option('--connection-string', default='postgresql://radar:password@localhost/radar')
@click.pass_context
def cli(ctx, connection_string):
    config = {
        'SQLALCHEMY_DATABASE_URI': connection_string,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'BASE_URL': 'http://localhost',
        'PASSWORD_HASH_METHOD': 'pbkdf2:sha1:1',
    }

    ctx.obj['app'] = Radar(config)


@cli.command()
@click.pass_context
def drop(ctx):
    with ctx.obj['app'].app_context():
        do_drop()
        db.session.commit()


@cli.command()
@click.pass_context
def create(ctx):
    with ctx.obj['app'].app_context():
        do_create()
        db.session.commit()


@cli.command()
@click.option('--patients', default=5)
@click.option('--password', default='password')
@click.pass_context
def all(ctx, patients, password):
    with ctx.obj['app'].app_context():
        do_drop()
        do_create()
        create_data(patients=patients, password=password)
        db.session.commit()


@cli.command()
@click.option('--patients', default=5)
@click.option('--data/--no-data', default=True)
@click.pass_context
def patients(ctx, patients, data):
    with ctx.obj['app'].app_context():
        create_patients(patients, data)
        db.session.commit()


@cli.command()
@click.option('--password', default='password')
@click.pass_context
def users(ctx, password):
    with ctx.obj['app'].app_context():
        create_bot_user(password)
        create_users(password)
        db.session.commit()


if __name__ == '__main__':
    cli(obj={})
