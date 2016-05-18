import os
import tempfile

from fabric.api import task, local, run, cd, get, put


@task
def build(rev='HEAD'):
    tmp = tempfile.mktemp(suffix='.tar.gz')
    local('git archive "%s" | gzip > "%s"' % (rev, tmp))

    build_tmp = '/tmp/build-%s' % os.urandom(20).encode('hex')
    run('mkdir %s' % build_tmp)
    put(tmp, '%s/src.tar.gz' % build_tmp)

    with cd(build_tmp):
        run('tar xzf src.tar.gz')
        run('PATH=/usr/pgsql-9.4/bin:$PATH platter build -r requirements.txt .')
        local('mkdir -p dist')
        get('dist/*.tar.gz', 'dist')

    run('rm -rf %s' % build_tmp)


@task
def deploy(archive=None):
    if archive is None:
        archive = os.path.join('dist', sorted(os.listdir('dist'))[-1])

    put(archive, '/tmp/radar.tar.gz')
    run('rm -rf /tmp/radar && mkdir -p /tmp/radar')

    with cd('/tmp/radar'):
        run('tar --strip-components=1 -xzf /tmp/radar.tar.gz')
        version = str(run('cat VERSION'))
        run('rm -rf /srv/radar/%s' % version)
        run('./install.sh /srv/radar/%s' % version)
        run('ln -sfn /srv/radar/%s /srv/radar/current' % version)

    run('rm -rf /tmp/radar /tmp/radar.tar.gz')
