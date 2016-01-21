import click

from radar.app import create_app
from radar.database import db
from radar_fixtures import create_data


@click.command()
@click.option('--connection-string', default='postgresql://radar:password@localhost/radar')
@click.option('--patients', default=5)
@click.option('--password', default='password')
def cli(connection_string, patients, password):
    config = {
        'SQLALCHEMY_DATABASE_URI': connection_string,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'BASE_URL': 'http://localhost',
        'PASSWORD_HASH_METHOD': 'pbkdf2:sha1:1000',
    }

    app = create_app(config)

    with app.app_context():
        db.drop_all()
        db.create_all()
        create_data(patients=patients, password=password)
        db.session.commit()


if __name__ == '__main__':
    cli()
