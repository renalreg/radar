#!/usr/bin/env python

import sys

import click

from radar.app import Radar
from radar.database import db, do_drop, do_create
from radar.database.utils import pg_restore, pg_dump


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
@click.argument('src')
def restore(src):
    # Note: --disable-triggers means the user must be a PostgreSQL superuser
    args = ['--data-only', '--disable-triggers', src]
    r = pg_restore(args)
    sys.exit(r)


@cli.command()
@click.argument('dest')
def dump(dest):
    tables = [
        'codes',
        'consultants',
        'diagnoses',
        'diagnosis_codes',
        'drug_groups',
        'drugs',
        'forms',
        'group_consultants',
        'group_diagnoses',
        'group_forms',
        'group_observations',
        'group_pages',
        'group_questionnaires',
        'groups',
        'observations',
        'specialties',
    ]

    args = ['-Fc']

    for table in tables:
        args += ['--table', table]

    with open(dest, 'w') as f:
        r = pg_dump(args, f)

    sys.exit(r)


def main():
    app = Radar()

    with app.app_context():
        cli()


if __name__ == '__main__':
    main()
