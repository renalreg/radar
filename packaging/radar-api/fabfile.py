import os
import re

from fabric.api import task, put, run, cd


@task
def deploy(archive=None, name='radar-api'):
    if archive is None:
        # Use the latest archive by default
        archive = sorted(x for x in os.listdir('.') if x.endswith('.tar.gz'))[-1]

    version = re.search('-([^-]+-[^-]+)\.tar\.gz$', archive).group(1)

    tmp_archive_path = '/tmp/%s.tar.gz' % name
    put(archive, tmp_archive_path)

    tmp_path = '/tmp/%s' % name
    run('rm -rf {path} && mkdir -p {path}'.format(path=tmp_path))

    current_version = '/srv/{name}/current'.format(name=name)
    new_version = '/srv/{name}/{version}'.format(name=name, version=version)

    with cd(tmp_path):
        run('tar --strip-components=1 -xzf %s' % tmp_archive_path)
        run('./install.sh %s' % new_version)

    run('ln -sfn %s %s' % (new_version, current_version))
    run('rm -rf %s' % tmp_archive_path)
