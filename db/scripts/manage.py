from functools import update_wrapper

import click

from radar.data.dev import create_users
from radar.app import create_app
from radar.database import db
from radar.data import dev, create_initial_data


def app_context(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        with ctx.obj['app'].app_context():
            return ctx.invoke(f, *args, **kwargs)

    return update_wrapper(new_func, f)


@click.group()
@click.option('--host', default='localhost')
@click.option('--port', default=5432)
@click.option('--username', default='radar')
@click.option('--password', default='vagrant')
@click.option('--database', default='radar')
@click.pass_context
def cli(ctx, host, port, username, password, database):
    connection_string = 'postgresql://{username}:{password}@{host}:{port}/{database}'.format(
        host=host,
        port=port,
        username=username,
        password=password,
        database=database,
    )

    config = {
        'SQLALCHEMY_DATABASE_URI': connection_string
    }

    ctx.obj['app'] = create_app(config)


@cli.command('initdb')
@app_context
def initdb():
    db.create_all()
    create_initial_data()


@cli.command('devdb')
@click.option('--patients', default=5)
@app_context
def devdb(patients):
    db.drop_all()
    db.create_all()
    dev.create_data(patients)
    db.session.commit()


@cli.command('devusers')
@click.option('--count', default=100)
@app_context
def devusers(count):
    create_users(count)
    db.session.commit()


if __name__ == '__main__':
    cli(obj={})
