import logging

import click

from utils import info, heading, success, Package

NAME = 'radar-web'
VERSION = '0.1.0'
ARCHITECTURE = 'noarch'
URL = 'http://www.radar.nhs.uk/'

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def package_web():
    heading('Package web')
    info('Version is %s' % VERSION)
    info('Building rpm ...')

    package = Package(NAME, VERSION, ARCHITECTURE, URL)
    package.add_dependency('radar-api')
    package.add_dependency('radar-client')
    package.add_dependency('nginx')

    paths = [
        ('web/nginx.conf', '/etc/nginx/conf.d/%s.conf' % NAME, True),
    ]

    for src, dst, config_file in paths:
        package.add_path(src, dst)

        if config_file:
            package.add_config_file(dst)

    rpm_path = package.build()

    success('Successfully built rpm at %s' % rpm_path)


@click.command()
def main():
    package_web()


if __name__ == '__main__':
    main()
