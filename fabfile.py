from contextlib import contextmanager
import binascii
import os
import tempfile

from fabric.api import task, local, run, cd, get, put, prompt, env, abort
from pkg_resources import parse_version

DEFAULT_DIST_DIR = 'dist'


@contextmanager
def temp():
    randomstr = binascii.hexlify(os.urandom(20)).decode('utf-8')
    tmp = '/tmp/radar-{0}'.format(randomstr)
    run('mkdir {0}'.format(tmp))

    with cd(tmp):
        yield

    run('rm -rf {0}'.format(tmp))


@task
def build(rev='HEAD'):
    archive = tempfile.mktemp(suffix='.tar.gz')
    local('git archive "{rev}" | gzip > "{archive}"'.format(rev=rev, archive=archive))

    with temp():
        put(archive, 'src.tar.gz')
        run('tar -xzf src.tar.gz')
        run('PATH=/usr/pgsql-9.4/bin:$PATH platter build --virtualenv-version 15.1.0 -r requirements.txt .')
        if not os.path.exists(DEFAULT_DIST_DIR):
            os.makedirs(DEFAULT_DIST_DIR)
        get('dist/*.tar.gz', DEFAULT_DIST_DIR)


@task
def deploy(archive=None, name='radar'):
    if archive is None:
        archive = os.path.join('dist', sorted(os.listdir('dist'), key=parse_version)[-1])

    with temp():
        put(archive, 'radar.tar.gz')
        run('tar --strip-components=1 -xzf radar.tar.gz')

        version = str(run('cat VERSION'))
        current_version = '/srv/{name}/current'.format(name=name)
        new_version = '/srv/{name}/{version}'.format(name=name, version=version)

        run('rm -rf {0}'.format(new_version))
        run('./install.sh {0}'.format(new_version))
        run('ln -sfn {0} {1}'.format(new_version, current_version))

    services = [
        'radar-admin',
        'radar-api',
        'radar-ukrdc-exporter-celery',
        'radar-ukrdc-importer-api',
        'radar-ukrdc-importer-celery',
    ]

    # Restart services
    # TODO replace with try-reload-or-restart when available in our version of systemd
    for service in services:
        run('if systemctl is-active {0} >/dev/null; then systemctl reload-or-restart {0}; fi'.format(service))


@task
def dump():
    with temp():
        run_db('dump radar.sql')
        get('radar.sql', '.')


def run_db(args):
    run('RADAR_SETTINGS=/etc/radar-api/settings.py /srv/radar/current/bin/radar-db {0}'.format(args))


def run_fixtures(args):
    run('RADAR_SETTINGS=/etc/radar-api/settings.py /srv/radar/current/bin/radar-fixtures {0}'.format(args))


@task
def staging():
    answer = prompt('Are you sure you want to DELETE ALL DATA on "{0}" and replace it with test data? (type "I am sure" to continue):'.format(env.host_string))

    if answer != 'I am sure':
        abort('Aborted!')

    run_fixtures('all')


@task
def demo():
    answer = prompt('Are you sure you want to DELETE ALL DATA on "{0}" and replace it with demo data? (type "I am sure" to continue):'.format(env.host_string))

    if answer != 'I am sure':
        abort('Aborted!')

    password = None

    while not password:
        password = prompt('Choose a password:')

    with temp():
        put('radar.sql', 'radar.sql')
        run_db('drop')
        run_db('create')
        run_db('restore radar.sql')  # Note: user must be a PostgreSQL superuser to run this
        run_fixtures('users --password {0}'.format(password))
        run_fixtures('patients --patients 95 --no-data')
        run_fixtures('patients --patients 5 --data')
