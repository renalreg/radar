import logging

import os

from packaging.radar import install_radar
from utils import run_command

PATH = ':'.join([
    '/usr/pgsql-9.4/bin',
    '/usr/local/bin',
    '/usr/bin',
    '/bin',
])


def install_api(v, src_directory='.'):
    logging.info('Installing api dependencies ...')
    requirements_path = os.path.join(src_directory, 'requirements.txt')
    v.install_requirements(requirements_path, env={'PATH': PATH})

    radar_path = os.path.join(src_directory, '../radar')
    install_radar(v, radar_path)

    logging.info('Installing api ...')
    v.run(['setup.py', 'install'], cwd=src_directory)


def package_api(v, src_directory='.'):
    install_directory = '/opt/radar-api'

    logging.info('Packaging radar ...')
    logging.info('Install directory is %s' % install_directory)

    # Update build path references to install path
    logging.info('Updating build virtualenv paths ...')
    v.relocate(install_directory)

    name = 'radar-api'
    version = v.run(['setup.py', '--version'], cwd=src_directory).strip()
    architecture = 'x86_64'
    rpm_path = '%s-%s.%s.rpm' % (name, version, architecture)

    logging.info('Version is %s' % version)

    # Package with fpm
    logging.info('Building rpm ...')
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

    logging.info('Successfully built rpm at %s' % rpm_path)
