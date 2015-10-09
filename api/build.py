import tempfile
import logging

import click

from packaging.api import install_api, package_api
from packaging.utils import run_command, get_python, Virtualenv

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


@click.command()
@click.option('--tox/--no-tox', default=True)
def build(tox):
    python = get_python()

    if tox:
        run_command(['tox', '-c', '../radar/tox.ini'])
        run_command(['tox'])

    with Virtualenv(tempfile.mkdtemp(), python) as v:
        install_api(v)
        package_api(v)
