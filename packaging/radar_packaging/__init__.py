from __future__ import print_function
from paramiko import SSHClient, AutoAddPolicy

import json
import subprocess
import logging
import shutil
import os
import select
import sys

import tox.config
import tox.session
import virtualenv_tools
import delorean

__version__ = '0.1.0'

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

    def install_requirements(self, path, env=None):
        head, tail = os.path.split(path)
        self.pip(['install', '-r', tail], env=env, cwd=head)

    def pip(self, arguments, env=None, cwd=None):
        command = [os.path.join(self.path, 'bin/pip')] + arguments
        return run_command(command, env=env, cwd=cwd)

    def delete(self):
        info('Deleting virtualenv at %s ...' % self.path)
        shutil.rmtree(self.path)

    def __enter__(self):
        self.create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()


class ANY(object):
    pass


def get_command_output(stdout, stderr):
    poll = select.poll()
    poll.register(stdout, select.POLLIN | select.POLLHUP)
    poll.register(stderr, select.POLLIN | select.POLLHUP)
    poll_count = 2

    events = poll.poll()
    output = []

    while poll_count > 0 and len(events) > 0:
        for event in events:
            f, event = event

            if event & select.POLLIN:
                if f == stdout.fileno():
                    line = stdout.readline()

                    if len(line) > 0:
                        output.append(line)
                        print(line, end='')
                elif f == stderr.fileno():
                    line = stderr.readline()

                    if len(line) > 0:
                        print(line, end='', file=sys.stderr)

            if event & select.POLLHUP:
                poll_count -= 1
                poll.unregister(f)

        if poll_count > 0:
            events = poll.poll()

    output = ''.join(output)

    return output


def check_exit_code(exit_code, allowed_exit_codes=None):
    if allowed_exit_codes is None:
        allowed_exit_codes = [0]

    if allowed_exit_codes is not ANY and exit_code not in allowed_exit_codes:
        error('Command exited with code %d' % exit_code)
        raise SystemExit(1)


def run_command(args, env=None, cwd=None, allowed_exit_codes=None):
    if cwd is None:
        cwd = os.getcwd()

    if env is None:
        env = {}

    if 'HTTP_PROXY' in os.environ:
        env.setdefault('HTTP_PROXY', os.environ['HTTP_PROXY'])

    if 'HTTPS_PROXY' in os.environ:
        env.setdefault('HTTPS_PROXY', os.environ['HTTPS_PROXY'])

    info('Running {args} with environment {env} and working directory {cwd}'.format(
        args=args,
        env=env,
        cwd=cwd,
    ))

    p = subprocess.Popen(args, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    output = get_command_output(p.stdout, p.stderr)
    exit_code = p.wait()

    check_exit_code(exit_code, allowed_exit_codes)

    return exit_code, output


def git(arguments, env=None, cwd=None, allowed_exit_codes=None):
    return run_command(['git'] + arguments, env=env, cwd=cwd, allowed_exit_codes=allowed_exit_codes)


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
    def __init__(self, name, version, release, architecture, url):
        self.name = name
        self.version = version
        self.architecture = architecture
        self.after_install = None
        self.before_install = None
        self.after_remove = None
        self.before_remove = None
        self.after_upgrade = None
        self.before_upgrade = None
        self.url = url
        self.release = release
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
        rpm_path = '%s-%s-%s.%s.rpm' % (self.name, self.version, self.release, self.architecture)

        args = [
            'fpm',
            '-s', 'dir',
            '-t', 'rpm',
            '--package', rpm_path,
            '--name', self.name,
            '--version', str(self.version),
            '--iteration', str(self.release),
            '--url', self.url,
            '--architecture', self.architecture,
            '--force',
        ]

        for package_name in self.dependencies:
            args.extend(['--depends', package_name])

        for path in self.config_files:
            args.extend(['--config-files', path])

        if self.after_install is not None:
            args.extend(['--after-install', self.after_install])

        if self.before_install is not None:
            args.extend(['--before-install', self.before_install])

        if self.after_remove is not None:
            args.extend(['--after-remove', self.after_remove])

        if self.before_remove is not None:
            args.extend(['--before-remove', self.before_remove])

        if self.after_upgrade is not None:
            args.extend(['--after-upgrade', self.after_upgrade])

        if self.before_upgrade is not None:
            args.extend(['--before-upgrade', self.before_upgrade])

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


def get_mock_ukrdc_src_path(root_path):
    return os.path.join(root_path, 'mock_ukrdc')


class Git(object):
    def __init__(self, path='.'):
        self.path = path

    def commit_date(self):
        output = git(['log', '-n', '1', '--format=%cd', '--date=iso'], cwd=self.path)[1].strip()
        return delorean.parse(output).datetime

    def branch(self):
        output = git(['symbolic-ref', 'HEAD'], cwd=self.path)[1].strip()
        return output

    def dirty(self):
        status = git(['status', '--porcelain'], cwd=self.path)[1].strip()
        return len(status) > 0


class Server(object):
    def __init__(self, hostname, port=22, username=None, password=None, key_filename=None):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(hostname, port=port, username=username, password=password, key_filename=key_filename)

    def run_command(self, command, allowed_exit_codes=None):
        channel = self.client.get_transport().open_session()
        channel.set_combine_stderr(True)
        channel.exec_command(command)

        f = channel.makefile()
        output = []

        for line in iter(f.readline, ''):
            print(line, end='')
            output.append(line)

        output = ''.join(output)

        exit_code = channel.recv_exit_status()
        check_exit_code(exit_code, allowed_exit_codes)

        return exit_code, output


def get_release(release):
    git = Git()

    if git.branch() != 'refs/heads/production':
        commit_date = git.commit_date()
        release = commit_date.strftime('0.%Y%m%d%H%M%S')

    return release
