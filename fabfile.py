from fabric.api import *


def staging():
    env.user = 'radar'
    env.hosts = ['radar-test.renalregistry.northbristol.local']

def pack():
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    dist = local('python setup.py --fullname', capture=True).strip()
    put('dist/%s.tar.gz' % dist, '/tmp/radar.tar.gz')

    run('rm -rf /tmp/radar')
    run('mkdir /tmp/radar')

    with cd('/tmp/radar'):
        run('tar xzf /tmp/radar.tar.gz')

    with cd('/tmp/radar/%s' % dist):
        run('/home/radar/envs/radar/bin/python setup.py install')

    run('rm -rf /tmp/radar /tmp/radar.tar.gz')
