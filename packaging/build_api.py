import tempfile
import logging

import click
import os

from utils import get_python, Virtualenv, run_tox, info, heading, success, Package
from build_radar import install_radar

NAME = 'radar-api'
ARCHITECTURE = 'x86_64'
URL = 'http://www.radar.nhs.uk/'

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

PATH = ':'.join([
    '/usr/pgsql-9.4/bin',
    '/usr/local/bin',
    '/usr/bin',
    '/bin',
])


def install_api(v, src_path):
    heading('Install api')

    info('Installing api dependencies ...')
    requirements_path = os.path.join(src_path, 'requirements.txt')
    v.install_requirements(requirements_path, env={'PATH': PATH})

    radar_path = os.path.join(src_path, '../radar')
    install_radar(v, radar_path)

    info('Installing api ...')
    v.run(['setup.py', 'install'], cwd=src_path)


def package_api(v, src_path):
    version = v.run(['setup.py', '--version'], cwd=src_path).strip()
    etc_path = '/etc/' + NAME
    install_path = '/opt/' + NAME

    heading('Package api')
    info('Version is %s' % version)

    # Update build path references to install path
    info('Updating build virtualenv paths ...')
    v.relocate(install_path)

    info('Building rpm ...')

    package = Package(NAME, version, ARCHITECTURE, URL)
    package.add_dependency('python')

    paths = [
        (v.path + '/', install_path, False),
        ('api/settings.py', etc_path + '/settings.py', True),
        ('api/gunicorn.py', etc_path + '/gunicorn.py', True),
        ('api/sysconfig', '/etc/sysconfig/' + name, True),
        ('api/systemd', '/etc/systemd/system/%s.service' % name, False),
    ]

    for src, dst, config_file in paths:
        package.add_path(src, dst)

        if config_file:
            package.add_config_file(dst)

    package.before_install_script = 'before_install.sh'
    rpm_path = package.build()

    success('Successfully built rpm at %s' % rpm_path)


@click.command()
@click.option('--enable-tox/--disable-tox', default=True)
def main(enable_tox):
    python = get_python()

    if enable_tox:
        run_tox(['-c', '../radar/tox.ini'])
        run_tox(['-c', '../api/tox.ini'])

    with Virtualenv(tempfile.mkdtemp(), python) as v:
        src_path = '../api'
        install_api(v, src_path)
        package_api(v, src_path)


if __name__ == '__main__':
    main()
