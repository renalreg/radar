import os
import tempfile

from fabric.api import task, local, run, cd, get, put


@task
def build(rev='HEAD'):
    archive = tempfile.mktemp(suffix='.tar.gz')
    local('git archive "{rev}" | gzip > "{archive}"'.format(rev=rev, archive=archive))

    tmp = '/tmp/build-{0}'.format(os.urandom(20).encode('hex'))
    run('mkdir {0}'.format(tmp))
    put(archive, '{0}/src.tar.gz'.format(tmp))

    with cd(tmp):
        run('tar -xzf src.tar.gz')
        run('PATH=/usr/pgsql-9.4/bin:$PATH platter build -r requirements.txt .')
        local('mkdir -p dist')
        get('dist/*.tar.gz', 'dist')

    run('rm -rf {0}'.format(tmp))


@task
def deploy(archive=None, name='radar'):
    if archive is None:
        archive = os.path.join('dist', sorted(os.listdir('dist'))[-1])

    tmp = '/tmp/deploy-{0}'.format(os.urandom(20).encode('hex'))
    run('mkdir {0}'.format(tmp))

    with cd(tmp):
        put(archive, 'radar.tar.gz')
        run('tar --strip-components=1 -xzf radar.tar.gz')

        version = str(run('cat VERSION'))
        current_version = '/srv/{name}/current'.format(name=name)
        new_version = '/srv/{name}/{version}'.format(name=name, version=version)

        run('rm -rf {0}'.format(new_version))
        run('./install.sh {0}'.format(new_version))
        run('ln -sfn {0} {1}'.format(new_version, current_version))

    run('rm -rf {0}'.format(tmp))

    services = [
        'radar-api',
        'radar-ukrdc-exporter-celery',
        'radar-ukrdc-importer-api',
        'radar-ukrdc-importer-celery',
    ]

    # Restart services
    # TODO replace with try-reload-or-restart when available in our version of systemd
    for service in services:
        run('if systemctl is-active {0} >/dev/null; then systemctl reload-or-restart {0}; fi'.format(service))
