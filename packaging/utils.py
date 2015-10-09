from subprocess import check_output, CalledProcessError
import subprocess
import logging
import shutil

import os
import re
import tox.config
import tox.session

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
    logging.info(BOLD + '===== ' + x + ' =====' + END)


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
        command = self.command(['-u'] + args)
        return run_command(command, env=env, cwd=cwd)

    @classmethod
    def clone(cls, path):
        return cls(path)


class Virtualenv(object):
    def __init__(self, path, python):
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
        env = {'PYTHONDONTWRITEBYTECODE': '1'}
        self.python.run(args, env=env)

    def run(self, args, env=None, cwd=None):
        if env is None:
            env = {}

        new_env = {'PYTHONDONTWRITEBYTECODE': '1'}
        new_env.update(env)

        return self.venv_python.run(args, env=new_env, cwd=cwd)

    def relocate(self, path):
        python = self.python.clone(os.path.join(path, 'bin/python'))
        bin_path = os.path.join(self.path, 'bin')
        shebang_regex = re.compile('^#!' + re.escape(self.venv_python.path))
        new_shebang = '#!%s' % python.path

        for filename in os.listdir(bin_path):
            filename = os.path.join(bin_path, filename)

            if not os.path.isfile(filename) or os.path.islink(filename):
                continue

            f = open(filename, 'rb')
            data = f.read()
            f.close()

            update = False

            if shebang_regex.match(data):
                data = shebang_regex.sub(new_shebang, data)
                info('Updated shebang in %s' % filename)
                update = True

            if self.path in data:
                data = data.replace(self.path, path)
                info('Updated path in %s' % filename)
                update = True

            if update:
                f = open(filename, 'wb')
                f.write(data)
                f.close()

    def install_package(self, package_name, env=None):
        self.run(['-m', 'pip', 'install', package_name], env=env)

    def install_requirements(self, path, env=None):
        cwd = os.path.dirname(path)
        self.run(['-m', 'pip', 'install', '-r', path], env=env, cwd=cwd)

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
        cwd=cwd
    ))

    try:
        return check_output(args, env=env, cwd=cwd, stderr=subprocess.STDOUT)
    except CalledProcessError as e:
        print e.output
        error('Command exited with code %d' % e.returncode)
        raise SystemExit(1)


def get_python():
    return Python('/usr/bin/python2.7')


def run_tox(args):
    config = tox.config.parseconfig(args)
    return_code = tox.session.Session(config).runcommand()

    if return_code != 0:
        raise SystemExit(1)
