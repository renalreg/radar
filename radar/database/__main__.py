#!/usr/bin/env python

import click

from radar.app import Radar
from radar.database import db, do_drop, do_create


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


def main():
    app = Radar()

    with app.app_context():
        cli()


if __name__ == '__main__':
    main()
