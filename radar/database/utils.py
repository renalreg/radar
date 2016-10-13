import os
import subprocess
from urlparse import urlparse

from radar.config import config


def pg_args(connection_string):
    u = urlparse(connection_string)

    args = []
    args += ['-h', u.hostname]
    args += ['-d', u.path[1:]]

    if u.port:
        args += ['-p', str(u.port)]

    if u.username:
        args += ['-U', u.username]

    return args

def pg_password(connection_string):
    return urlparse(connection_string).password


def pg_restore(args):
    connection_string = config['SQLALCHEMY_DATABASE_URI']

    environment = os.environ.copy()
    command = ['pg_restore'] + pg_args(connection_string) + args

    password = pg_password(connection_string)

    if password is not None:
        environment['PGPASSWORD'] = password

    print environment
    print command

    p = subprocess.Popen(command, env=environment)
    return p.wait()
