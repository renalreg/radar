from subprocess import check_output, CalledProcessError
import subprocess
import logging
import os
import errno
from pipes import quote
import sys
import stat
import re


class Python(object):
    def __init__(self, path):
        self.path = path

    def exists(self):
        return os.path.exists(self.path)

    def command(self, args=None):
        if args is None:
            args = []

        return [self.path] + args

    def wrapper(self):
        command = self.command()
        sh = '#!/bin/sh\nexec %s' % ' '.join(command)
        return sh

    def create_wrapper(self, wrapper_path):
        sh = self.wrapper()

        with open(wrapper_path, 'wb') as f:
            f.write(sh)
            os.fchmod(f.fileno(), stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    def run(self, args, env=None, cwd=None):
        command = self.command(['-u'] + args)
        return run_command(command, env=env, cwd=cwd)

    @classmethod
    def clone(cls, path):
        return cls(path)


class SCLPython(Python):
    def command(self, args=None):
        if args is None:
            args = []

        return ['scl', 'enable', 'python27', join_args([self.path] + args)]


class Virtualenv(object):
    def __init__(self, path, python):
        self.path = path
        self.python = python

        venv_python_path = os.path.join(self.path, 'bin/python')
        self.venv_python = python.clone(venv_python_path)

    def create(self):
        logging.info('Creating virtualenv at %s' % self.path)

        args = [
            '-m', 'virtualenv',
            '--quiet',
            self.path
        ]
        env = {'PYTHONDONTWRITEBYTECODE': '1'}
        self.python.run(args, env=env)

        mkdir_p(os.path.dirname(self.venv_python.path))
        self.venv_python.create_wrapper(self.venv_python.path + '.sh')

    def run(self, args, env=None, cwd=None):
        if env is None:
            env = {}

        new_env = {'PYTHONDONTWRITEBYTECODE': '1'}
        new_env.update(env)

        return self.venv_python.run(args, env=new_env, cwd=cwd)

    def relocate(self, path):
        wrapper_path = self.venv_python.path + '.sh'
        python = self.python.clone(os.path.join(path, 'bin/python'))
        python.create_wrapper(wrapper_path)
        wrapper_path = python.path + '.sh'
        bin_path = os.path.join(self.path, 'bin')
        shebang_regex = re.compile('^#!' + re.escape(self.venv_python.path))
        new_shebang = '#!%s' % wrapper_path

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
                logging.info('Updated shebang in %s' % filename)
                update = True

            if self.path in data:
                data = data.replace(self.path, path)
                logging.info('Updated path in %s' % filename)
                update = True

            if update:
                f = open(filename, 'wb')
                f.write(data)
                f.close()


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def join_args(args):
    return ' '.join(quote(x) for x in args)


def run_command(args, env=None, cwd=None):
    if cwd is None:
        cwd = os.getcwd()

    if env is None:
        env = {}

    logging.info('Running {args} with environment {env} and working directory {cwd}'.format(
        args=args,
        env=env,
        cwd=cwd
    ))

    try:
        return check_output(args, env=env, cwd=cwd, stderr=subprocess.STDOUT)
    except CalledProcessError as e:
        print e.output
        raise


def relative_to_script(relative_path):
    script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    path = os.path.abspath(os.path.join(script_path, relative_path))
    return path


def get_python():
    pythons = [
        Python('/usr/bin/python2.7'),
        SCLPython('/opt/rh/python27/root/usr/bin/python2.7'),
    ]

    for x in pythons:
        if x.exists():
            return x
    else:
        raise ValueError('No python interpreter found!')
