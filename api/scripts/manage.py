import click
from radar.data.dev import create_users

from radar_api.app import create_app
from radar.database import db
from radar.data import dev, create_initial_data


@click.group()
def cli():
    pass


@cli.command('initdb')
def initdb():
    db.create_all()
    create_initial_data()


@cli.command('devdb')
@click.option('--patients', default=5)
def devdb(patients):
    db.drop_all()
    db.create_all()
    dev.create_data(patients)
    db.session.commit()


@cli.command('devusers')
@click.option('--count', default=100)
def devusers(count):
    create_users(count)
    db.session.commit()


@cli.command('runserver')
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5001)
def runserver(host, port):
    app.run(host=host, port=port)


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        cli()
