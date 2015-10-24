import json
from subprocess import check_output, CalledProcessError
import subprocess
import logging
import shutil
import os

import tox.config
import tox.session
import virtualenv_tools

PURPLE = '\033[95m'
CYAN = '\033[96m'
DARK_CYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'


def heading(x):
    logging.info(BOLD + '========== ' + x + ' ==========' + END)


def error(x):
    logging.error(RED + x + END)


def info(x):
    logging.info(x)


def success(x):
    logging.info(GREEN + x + END)


class Python(object):
    def __init__(self, path):
        self.path = path

    def exists(self):
        return os.path.exists(self.path)

    def command(self, args=None):
        if args is None:
            args = []

        return [self.path] + args

    def run(self, args, env=None, cwd=None):
        if env is None:
            env = {}

        env['PYTHONUNBUFFERED'] = '1'

        command = self.command(args)

        return run_command(command, env=env, cwd=cwd)

    @classmethod
    def clone(cls, path):
        return cls(path)


class Virtualenv(object):
    def __init__(self, path, python=None):
        if python is None:
            python = get_python()

        self.path = path
        self.python = python

        venv_python_path = os.path.join(self.path, 'bin/python')
        self.venv_python = python.clone(venv_python_path)

    def create(self):
        info('Creating virtualenv at %s ...' % self.path)

        args = [
            '-m', 'virtualenv',
            '--quiet',
            self.path
        ]

        self.python.run(args)

    def run(self, args, env=None, cwd=None):
        return self.venv_python.run(args, env=env, cwd=cwd)

    def update_paths(self, new_path):
        virtualenv_tools.update_paths(self.path, new_path)

    def install_package(self, package_name, env=None):
        self.run(['-m', 'pip', 'install', package_name], env=env)

    def install_requirements(self, path, env=None):
        head, tail = os.path.split(path)
        self.run(['-m', 'pip', 'install', '-r', tail], env=env, cwd=head)

    def delete(self):
        info('Deleting virtualenv at %s ...' % self.path)
        shutil.rmtree(self.path)

    def __enter__(self):
        self.create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()


def run_command(args, env=None, cwd=None):
    if cwd is None:
        cwd = os.getcwd()

    if env is None:
        env = {}

    info('Running {args} with environment {env} and working directory {cwd}'.format(
        args=args,
        env=env,
        cwd=cwd,
    ))

    p = subprocess.Popen(args, cwd=cwd, env=env, bufsize=1)
    p.communicate()

    if p.returncode != 0:
        error('Command exited with code %d' % p.returncode)
        raise SystemExit(1)


def get_python():
    return Python('/usr/bin/python2.7')


def run_tox(args=None):
    if args is None:
        args = []

    config = tox.config.parseconfig(args)
    return_code = tox.session.Session(config).runcommand()

    if return_code != 0:
        raise SystemExit(1)


class Package(object):
    def __init__(self, name, version, architecture, url):
        self.name = name
        self.version = version
        self.architecture = architecture
        self.before_install_script = None
        self.url = url
        self.dependencies = []
        self.paths = []
        self.config_files = []

    def add_dependency(self, package_name):
        self.dependencies.append(package_name)

    def add_path(self, src, dst):
        self.paths.append('%s=%s' % (src, dst))

    def add_config_file(self, path):
        self.config_files.append(path)

    def build(self):
        rpm_path = '%s-%s.%s.rpm' % (self.name, self.version, self.architecture)

        args = [
            'fpm',
            '-s', 'dir',
            '-t', 'rpm',
            '--package', rpm_path,
            '--name', self.name,
            '--version', self.version,
            '--url', self.url,
            '--architecture', self.architecture,
            '--epoch', '0',
            '--force',
        ]

        for package_name in self.dependencies:
            args.extend(['--depends', package_name])

        for path in self.config_files:
            args.extend(['--config-files', path])

        if self.before_install_script is not None:
            args.extend(['--before-install', self.before_install_script])

        for path in self.paths:
            args.append(path)

        run_command(args, env={'PATH': '/usr/local/bin:/usr/bin:/bin'})

        return rpm_path


def get_version_from_package_json(path):
    try:
        package_data = open(path, 'rb').read()
    except IOError:
        return None

    package = json.loads(package_data)

    return package.get('version', None)


def get_api_src_path(root_path):
    return os.path.join(root_path, 'api')


def get_radar_src_path(root_path):
    return os.path.join(root_path, 'radar')


def get_client_src_path(root_path):
    return os.path.join(root_path, 'client')
