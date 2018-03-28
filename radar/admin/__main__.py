#!/usr/bin/env python

import click
from flask import abort, current_app

from radar.admin.app import RadarAdmin
from radar.auth.sessions import current_user


@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5002)
def start(host, port):
    current_app.run(host=host, port=port)


def restrict_admin_url(*args, **kwargs):
    authenticated = current_user.is_authenticated()
    if not authenticated or not current_user.is_admin:
        abort(404)


def main():
    app = RadarAdmin()
    app.before_request(restrict_admin_url)
    with app.app_context():
        start()


if __name__ == '__main__':
    main()
