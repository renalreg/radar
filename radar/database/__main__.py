#!/usr/bin/env python

import sys

import click

from radar.app import Radar
from radar.database import db, do_drop, do_create
from radar.database.utils import pg_restore


@click.group()
def cli():
    pass


@cli.command()
def drop():
    do_drop()
    db.session.commit()


@cli.command()
def create():
    do_create()
    db.session.commit()


@cli.command()
@click.argument('args', nargs=-1)
def restore(args):
    args = list(args)
    r = pg_restore(args)
    sys.exit(r)


def main():
    app = Radar()

    with app.app_context():
        cli()


if __name__ == '__main__':
    main()
