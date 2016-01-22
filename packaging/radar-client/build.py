#!/usr/bin/env python

import logging

import os
import click

from radar_packaging import run_command, heading, success, Package, get_version_from_package_json, info, error, \
    get_client_src_path, get_release

NAME = 'radar-client'
ARCHITECTURE = 'noarch'
URL = 'http://www.radar.nhs.uk/'
RELEASE = 1

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def run_gulp(task, env=None, cwd=None):
    run_command(['gulp', task, '--color'], env=env, cwd=cwd)


def build_client(root_path):
    src_path = get_client_src_path(root_path)

    heading('Build %s' % NAME)
    run_gulp('build:dist', cwd=src_path)


def package_client(root_path):
    src_path = get_client_src_path(root_path)

    heading('Package %s' % NAME)

    install_path = '/opt/radar-client'
    dist_path = os.path.join(src_path, 'dist')
    package_json_path = os.path.join(src_path, 'package.json')

    version = get_version_from_package_json(package_json_path)

    if version is None:
        error('No version in %s' % package_json_path)
        raise SystemExit(1)
    else:
        info('Version is %s' % version)

    release = get_release(RELEASE)
    info('Release is %s' % release)

    info('Building rpm ...')

    package = Package(NAME, version, release, ARCHITECTURE, URL)
    package.add_path(dist_path + '/', install_path)
    rpm_path = package.build()

    success('Successfully built rpm at %s' % rpm_path)


def test_client(root_path):
    src_path = get_client_src_path(root_path)

    heading('Test %s' % NAME)
    run_gulp('lint', cwd=src_path)
    run_gulp('test', cwd=src_path)


@click.command()
@click.option('--enable-tests/--disable-tests', default=True)
def main(enable_tests):
    root_path = os.path.abspath('../../')

    if enable_tests:
        test_client(root_path)

    build_client(root_path)
    package_client(root_path)


if __name__ == '__main__':
    main()
