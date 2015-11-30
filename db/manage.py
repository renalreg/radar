#!/usr/bin/env python

from functools import update_wrapper

import click

from radar.app import create_app
from radar.database import db
from radar.fixtures import dev, create_initial_data


def app_context(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        with ctx.obj['app'].app_context():
            return ctx.invoke(f, *args, **kwargs)

    return update_wrapper(new_func, f)


@click.group()
@click.option('--connection-string', default='postgresql:///radar')
@click.pass_context
def cli(ctx, connection_string):
    config = {
        'SQLALCHEMY_DATABASE_URI': connection_string,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }

    ctx.obj['app'] = create_app(config)


@cli.command('init')
@app_context
def init_command():
    db.create_all()
    create_initial_data()
    db.session.commit()


@cli.command('dev')
@click.option('--patients', default=5)
@click.option('--users', default=0)
@app_context
def dev_command(patients, users):
    db.drop_all()
    db.create_all()
    dev.create_data(patients, users)
    db.session.commit()


@cli.command('create')
@app_context
def create_command():
    db.create_all()
    db.session.commit()


@cli.command('drop')
@app_context
def drop_command():
    db.drop_all()
    db.session.commit()


if __name__ == '__main__':
    cli(obj={})
