import tempfile
import logging

import click
import os

from utils import get_python, Virtualenv, run_command, run_tox, info, heading, success
from package_radar import install_radar

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


def install_api(v, src_directory='.'):
    heading('Install api')

    info('Installing api dependencies ...')
    requirements_path = os.path.join(src_directory, 'requirements.txt')
    v.install_requirements(requirements_path, env={'PATH': PATH})

    radar_path = os.path.join(src_directory, '../radar')
    install_radar(v, radar_path)

    info('Installing api ...')
    v.run(['setup.py', 'install'], cwd=src_directory)


def package_api(v, src_directory='.'):
    install_directory = '/opt/radar-api'

    heading('Package api')
    info('Install directory is %s' % install_directory)

    # Update build path references to install path
    info('Updating build virtualenv paths ...')
    v.relocate(install_directory)

    info('Building rpm ...')
    name = 'radar-api'
    version = v.run(['setup.py', '--version'], cwd=src_directory).strip()
    architecture = 'x86_64'
    rpm_path = '%s-%s.%s.rpm' % (name, version, architecture)
    info('Version is %s' % version)
    run_command([
        'fpm',
        '-s', 'dir',
        '-t', 'rpm',
        '--package', rpm_path,
        '--name', name,
        '--version', version,
        '--url', 'http://www.radar.nhs.uk/',
        '--architecture', architecture,
        '--epoch', '0',
        '--force',
        '--depends', 'python',
        '%s/=%s' % (v.path, install_directory)
    ], env={'PATH': '/usr/local/bin:/usr/bin:/bin'})

    success('Successfully built rpm at %s' % rpm_path)


@click.command()
@click.option('--enable-tox/--disable-tox', default=True)
def package(enable_tox):
    python = get_python()

    if enable_tox:
        run_tox(['-c', '../radar/tox.ini'])
        run_tox(['-c', '../api/tox.ini'])

    with Virtualenv(tempfile.mkdtemp(), python) as v:
        install_api(v, '../api')
        package_api(v, '../api')


if __name__ == '__main__':
    package()
