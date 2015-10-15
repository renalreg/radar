import logging

import os
import click

from utils import run_command, heading, success, Package

NAME = 'radar-client'
ARCHITECTURE = 'noarch'
URL = 'http://www.radar.nhs.uk/'

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def build_client(src_path):
    heading('Build client')
    run_command(['gulp', 'build:dist'], cwd=src_path)


def package_client(src_path):
    install_path = '/opt/radar-client'
    dist_path = os.path.join(src_path, 'dist')

    # TODO version
    package = Package(NAME, '0.2.0', ARCHITECTURE, URL)
    package.add_path(dist_path + '/', install_path)
    rpm_path = package.build()

    success('Successfully built rpm at %s' % rpm_path)


@click.command()
def main():
    src_path = '../client'
    build_client(src_path)
    package_client(src_path)


if __name__ == '__main__':
    main()
