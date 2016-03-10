#!/usr/bin/env python

import logging
import tarfile
import os
import click

from radar_packaging import run_command, heading, success, get_version_from_package_json, info, error, \
    get_client_src_path, get_release
from radar_packaging.package_builder import PackageBuilder

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


def test_client(root_path):
    src_path = get_client_src_path(root_path)

    heading('Test %s' % NAME)
    run_gulp('lint', cwd=src_path)
    run_gulp('test', cwd=src_path)


def create_rpm(root_path):
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

    builder = PackageBuilder(NAME, version, release, ARCHITECTURE, URL)
    builder.add_path(dist_path + '/', install_path)
    rpm_path = builder.build()

    success('Successfully built rpm at %s' % rpm_path)


def create_tar(root_path):
    src_path = get_client_src_path(root_path)
    package_json_path = os.path.join(src_path, 'package.json')
    dist_path = os.path.join(src_path, 'dist')
    version = get_version_from_package_json(package_json_path)

    release = get_release(RELEASE)

    base_filename = '%s-%s-%s' % (NAME, version, release)
    filename = '%s.tar.gz' % base_filename

    base_filename = filename.rstrip('.tar.gz')

    def reset(tarinfo):
        tarinfo.uid = tarinfo.gid = 0
        tarinfo.uname = tarinfo.gname = 'root'

        if tarinfo.isdir():
            tarinfo.mode = 0755
        else:
            tarinfo.mode = 0644

        return tarinfo

    # Compress with gzip
    f = tarfile.open(filename, 'w:gz')
    f.add(dist_path, base_filename, filter=reset)
    f.close()

    success('Successfully built archive at %s' % filename)


RPM = 0
TAR = 1


@click.group()
def cli():
    pass


@cli.command()
@click.option('--enable-tests/--disable-tests', default=True)
def rpm(enable_tests):
    main(RPM, enable_tests)


@cli.command()
@click.option('--enable-tests/--disable-tests', default=True)
def tar(enable_tests):
    main(TAR, enable_tests)


def main(format, run_tests):
    root_path = os.path.abspath('../../')

    if run_tests:
        test_client(root_path)

    build_client(root_path)

    if format == RPM:
        create_rpm(root_path)
    else:
        create_tar(root_path)


if __name__ == '__main__':
    cli()
