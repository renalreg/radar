from collections import namedtuple
import os
import subprocess
from urlparse import urlparse

from radar.config import config


PostgreSQL = namedtuple('PostgreSQL', ['hostname', 'port', 'database', 'username', 'password'])


def pg_parse(connection_string):
    u = urlparse(connection_string)
    return PostgreSQL(u.hostname, u.port, u.path[1:], u.username, u.password)


def pg_dump(args, dest):
    connection_string = config['SQLALCHEMY_DATABASE_URI']
    pg = pg_parse(connection_string)

    environment = os.environ.copy()
    command = ['pg_dump']

    command += ['-h', pg.hostname]

    if pg.port:
        command += ['-p', str(pg.port)]

    if pg.username:
        command += ['-U', pg.username]

    if pg.password is not None:
        environment['PGPASSWORD'] = pg.password

    command += args

    command += [pg.database]

    print(environment)
    print(command)

    p = subprocess.Popen(command, env=environment, stdout=dest)
    return p.wait()


def pg_restore(args):
    connection_string = config['SQLALCHEMY_DATABASE_URI']
    pg = pg_parse(connection_string)

    environment = os.environ.copy()
    command = ['pg_restore']

    command += ['-h', pg.hostname]
    command += ['-d', pg.database]

    if pg.port:
        command += ['-p', str(pg.port)]

    if pg.username:
        command += ['-U', pg.username]

    if pg.password is not None:
        environment['PGPASSWORD'] = pg.password

    command += args

    print(environment)
    print(command)

    p = subprocess.Popen(command, env=environment)
    return p.wait()
