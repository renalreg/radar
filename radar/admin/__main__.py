#!/usr/bin/env python

import click
from flask import current_app

from radar.admin.app import RadarAdmin


@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5002)
def start(host, port):
    current_app.run(host=host, port=port)


def main():
    app = RadarAdmin()

    with app.app_context():
        start()


if __name__ == '__main__':
    main()
