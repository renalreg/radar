#!/usr/bin/env python

import logging

import click

from radar.api.app import RadarAPI


@click.group()
def cli():
    pass


@cli.command('runserver')
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5000)
def runserver(host, port):
    app.run(host=host, port=port)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    app = RadarAPI()

    with app.app_context():
        cli()
