from contextlib import contextmanager
import binascii
import os
from pathlib import Path
import tempfile

from fabric import task

from pkg_resources import parse_version

DEFAULT_DIST_DIR = "dist"

# run with
# fab -H root@some_host --prompt-for-login-password deploy|build


@contextmanager
def temp(c):
    randomstr = binascii.hexlify(os.urandom(20)).decode("utf-8")
    tmp = "/tmp/radar-{0}".format(randomstr)
    c.run("mkdir {0}".format(tmp))

    with c.cd(tmp):
        yield tmp

    c.run("rm -rf {0}".format(tmp))


@task
def build(c, rev="HEAD"):
    archive = tempfile.mktemp(suffix=".tar.gz")

    c.local(
        'git archive "{rev}" | gzip > "{archive}"'.format(rev=rev, archive=archive),
        env=os.environ
    )

    with temp(c) as cwd:
        c.put(archive, cwd + "/src.tar.gz")
        c.run("tar -xzf src.tar.gz")
        c.run(
            "PATH=/usr/pgsql-9.4/bin:$PATH "
            "platter build "
            "--virtualenv-version 15.1.0 "
            "-p python3 -r requirements.txt ."
        )
        if not os.path.exists(DEFAULT_DIST_DIR):
            os.makedirs(DEFAULT_DIST_DIR)
        result = c.run("ls " + cwd + "/dist/")
        fname = result.stdout.strip()
        c.get(cwd + "/dist/" + fname, os.path.join(DEFAULT_DIST_DIR, fname))

    path = Path(archive)
    if path.exists():
        path.unlink()


@task
def deploy(c, archive=None, name="radar"):
    if archive is None:
        archive = os.path.join("dist", sorted(os.listdir("dist"), key=parse_version)[-1])

    with temp(c) as cwd:
        c.put(archive, cwd + "/radar.tar.gz")
        c.run("tar --strip-components=1 -xzf radar.tar.gz")

        version = c.run("cat VERSION").stdout.strip()
        current_version = "/srv/{name}/current".format(name=name)
        new_version = "/srv/{name}/{version}".format(name=name, version=version)

        c.run("rm -rf {0}".format(new_version))
        c.run(cwd + "/install.sh {0}".format(new_version))
        c.run("ln -sfn {0} {1}".format(new_version, current_version))

    services = [
        "radar-admin",
        "radar-api",
        "radar-ukrdc-exporter-celery",
        "radar-ukrdc-importer-api",
        "radar-ukrdc-importer-celery",
    ]

    # Restart services
    # TODO replace with try-reload-or-restart when available in our version of systemd
    cmd = "if systemctl is-active {0} >/dev/null; then systemctl reload-or-restart {0}; fi"
    for service in services:
        print("Running: ", cmd.format(service))
        c.run(cmd.format(service))


# @task
# def dump():
#     with temp():
#         run_db('dump radar.sql')
#         get('radar.sql', '.')


# def run_db(args):
#     run(
#         "RADAR_SETTINGS=/etc/radar-api/settings.py /srv/radar/current/bin/radar-db {0}".format(
#             args
#         )
#     )


# def run_fixtures(args):
#     run(
#         "RADAR_SETTINGS=/etc/radar-api/settings.py /srv/radar/current/bin/radar-fixtures {0}".format(
#             args
#         )
#     )


# @task
# def staging():
#     answer = prompt(
#         'Are you sure you want to DELETE ALL DATA on "{0}" '
#         'and replace it with test data? (type "I am sure" to continue):'.format(
#             env.host_string
#         )
#     )

#     if answer != "I am sure":
#         abort("Aborted!")

#     run_fixtures("all")

#     run_fixtures('all')

# @task
# def demo():
#     answer = prompt(
#         'Are you sure you want to DELETE ALL DATA on "{0}" '
#         'and replace it with demo data? (type "I am sure" to continue):'.format(
#             env.host_string
#         )
#     )

#     if answer != "I am sure":
#         abort("Aborted!")

#     password = None

#     while not password:
#         password = prompt("Choose a password:")

#     with temp():
#         put("radar.sql", "radar.sql")
#         run_db("drop")
#         run_db("create")
#         run_db("restore radar.sql")  # Note: user must be a PostgreSQL superuser to run this
#         run_fixtures("users --password {0}".format(password))
#         run_fixtures("patients --patients 95 --no-data")
#         run_fixtures("patients --patients 5 --data")
