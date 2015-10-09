import click

from radar.api.app import create_app
from radar.lib.database import db
from radar.lib.data import dev, create_initial_data


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


@cli.command('runserver')
@click.option('--port', default=5001)
def run_server(port):
    app.run(port=port)


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        cli()
