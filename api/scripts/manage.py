#!/usr/bin/env python

import click

from radar_api.app import create_app


@click.group()
def cli():
    pass


@cli.command('runserver')
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5001)
def runserver(host, port):
    app.run(host=host, port=port)


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        cli()
