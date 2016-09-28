#!/usr/bin/env python

import logging

import click
from flask import current_app

from radar.api.app import RadarAPI


@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5000)
def start(host, port):
    current_app.run(host=host, port=port)


def main():
    logging.basicConfig(level=logging.INFO)

    app = RadarAPI()

    with app.app_context():
        start()


if __name__ == '__main__':
    main()
