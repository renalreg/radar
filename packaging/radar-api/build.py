#!/usr/bin/env python

import tempfile
import logging

import click
import os

from radar_packaging import Virtualenv, run_tox, info, heading, success, get_radar_src_path, \
    get_api_src_path, get_release, run_command
from radar_packaging.wheel_builder import WheelBuilder
from radar_packaging.package_builder import PackageBuilder

NAME = 'radar-api'
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


def install_api(v, root_path):
    api_src_path = get_api_src_path(root_path)
    radar_src_path = get_radar_src_path(root_path)

    heading('Install %s' % NAME)

    info('Installing radar ...')
    v.pip(['install', '--no-deps', '.'], cwd=radar_src_path)

    info('Installing radar-api dependencies ...')
    requirements_path = os.path.join(api_src_path, 'requirements.txt')
    v.install_requirements(requirements_path, env={'PATH': PATH})

    info('Installing radar-api ...')
    v.pip(['install', '--no-deps', '.'], cwd=api_src_path)


def get_version(path):
    return run_command(['python', 'setup.py', '--version'], cwd=path)[1].strip()


def package_api(v, root_path):
    src_path = get_api_src_path(root_path)

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

    builder = PackageBuilder(NAME, version, release, ARCHITECTURE, URL)
    builder.add_dependency('python')
    builder.add_dependency('postgresql94-libs')

    paths = [
        (v.path + '/', install_path, False),
        ('settings.py', etc_path + '/settings.py', True),
        ('uwsgi.ini', etc_path + '/uwsgi.ini', True),
        ('systemd', '/usr/lib/systemd/system/%s.service' % NAME, False),
    ]

    for src, dst, config_file in paths:
        builder.add_path(src, dst)

        if config_file:
            builder.add_config_file(dst)

    builder.before_install = 'before_install.sh'
    builder.after_install = 'after_install.sh'
    builder.after_upgrade = 'after_upgrade.sh'
    builder.before_remove = 'before_remove.sh'
    builder.after_remove = 'after_remove.sh'

    rpm_path = builder.build()

    success('Successfully built rpm at %s' % rpm_path)


def test_api(root_path):
    radar_src_path = get_radar_src_path(root_path)
    api_src_path = get_api_src_path(root_path)

    heading('Test %s' % NAME)
    run_tox(['-r', '-c', os.path.join(radar_src_path, 'tox.ini')])
    run_tox(['-r', '-c', os.path.join(api_src_path, 'tox.ini')])


@click.group()
def cli():
    pass


@cli.command('rpm')
@click.option('--enable-tests/--disable-tests', default=True)
def rpm(enable_tests):
    root_path = os.path.abspath('../../')

    if enable_tests:
        test_api(root_path)

    with Virtualenv(tempfile.mkdtemp()) as v:
        install_api(v, root_path)
        package_api(v, root_path)


@cli.command('tar')
@click.option('--enable-tests/--disable-tests', default=True)
def tar(enable_tests):
    root_path = os.path.abspath('../../')

    if enable_tests:
        test_api(root_path)

    radar_src_path = get_radar_src_path(root_path)
    api_src_path = get_api_src_path(root_path)

    version = get_version(api_src_path)
    release = get_release(RELEASE)

    archive_path = '%s-%s-%s.tar.gz' % (NAME, version, release)

    builder = WheelBuilder()
    builder.add(['--no-deps', '.'], cwd=radar_src_path)
    builder.add(['-r', 'requirements.txt'], cwd=api_src_path)
    builder.add(['--no-deps', '.'], cwd=api_src_path)
    builder.build(archive_path)
    builder.cleanup()

    success('Successfully built archive at %s' % archive_path)


if __name__ == '__main__':
    cli()
