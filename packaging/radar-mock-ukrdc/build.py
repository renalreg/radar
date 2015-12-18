#!/usr/bin/env python

import sys
sys.path.append('../')

import tempfile
import logging

import click
import os

from build_tools import Virtualenv, run_tox, info, heading, success, Package, get_radar_src_path, \
    get_mock_ukrdc_src_path, get_release

NAME = 'radar-mock-ukrdc'
ARCHITECTURE = 'x86_64'
URL = 'http://www.radar.nhs.uk/'
RELEASE = 1

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


def install_mock_ukrdc(v, root_path):
    mock_ukrdc_src_path = get_mock_ukrdc_src_path(root_path)
    radar_src_path = get_radar_src_path(root_path)

    heading('Install %s' % NAME)

    info('Installing radar ...')
    v.pip(['install', '--no-deps', '.'], cwd=radar_src_path)

    info('Installing radar-mock-ukrdc dependencies ...')
    requirements_path = os.path.join(mock_ukrdc_src_path, 'requirements.txt')
    v.install_requirements(requirements_path, env={'PATH': PATH})

    info('Installing radar-mock-ukrdc ...')
    v.pip(['install', '--no-deps', '.'], cwd=mock_ukrdc_src_path)


def package_mock_ukrdc(v, root_path):
    src_path = get_mock_ukrdc_src_path(root_path)

    version = v.run(['setup.py', '--version'], cwd=src_path)[1].strip()
    etc_path = '/etc/' + NAME
    install_path = '/opt/' + NAME

    heading('Package %s' % NAME)
    info('Version is %s' % version)

    release = get_release(RELEASE)
    info('Release is %s' % release)

    # Update build path references to install path
    info('Updating virtualenv paths ...')
    v.update_paths(install_path)

    info('Building rpm ...')

    package = Package(NAME, version, release, ARCHITECTURE, URL)
    package.add_dependency('python')

    paths = [
        (v.path + '/', install_path, False),
        ('settings.py', etc_path + '/settings.py', True),
        ('uwsgi.ini', etc_path + '/uwsgi.ini', True),
        ('systemd', '/usr/lib/systemd/system/%s.service' % NAME, False),
    ]

    for src, dst, config_file in paths:
        package.add_path(src, dst)

        if config_file:
            package.add_config_file(dst)

    package.before_install_script = '../before_install.sh'
    rpm_path = package.build()

    success('Successfully built rpm at %s' % rpm_path)


def test_mock_ukrdc(root_path):
    radar_src_path = get_radar_src_path(root_path)
    mock_ukrdc_src_path = get_mock_ukrdc_src_path(root_path)

    heading('Test %s' % NAME)
    run_tox(['-r', '-c', os.path.join(radar_src_path, 'tox.ini')])
    run_tox(['-r', '-c', os.path.join(mock_ukrdc_src_path, 'tox.ini')])


@click.command()
@click.option('--enable-tests/--disable-tests', default=True)
def main(enable_tests):
    root_path = os.path.abspath('../../')

    if enable_tests:
        test_mock_ukrdc(root_path)

    with Virtualenv(tempfile.mkdtemp()) as v:
        install_mock_ukrdc(v, root_path)
        package_mock_ukrdc(v, root_path)


if __name__ == '__main__':
    main()
