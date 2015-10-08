import shutil
from subprocess import check_output
import tempfile
import os
import errno
from pipes import quote


class Python(object):
    def __init__(self, path):
        self.path = path

    def exists(self):
        return os.path.exists(self.path)

    def command(self):
        return [self.path]

    def wrapper(self):
        command = self.command()
        sh = '#!/bin/sh\nexec %s' % ' '.join(command)
        return sh

    def create_wrapper(self, wrapper_path):
        sh = self.wrapper()

        with open(wrapper_path, 'wb') as f:
            f.write(sh)
            os.fchmod(f.fileno(), 755)

    def run(self, args, env=None):
        args = self.command() + args
        return run_command(args, env=env)

    @classmethod
    def copy_at_path(cls, path):
        return cls(path)


class SCLPython(Python):
    def command(self):
        return ['scl', 'enable', 'python27', self.path]

    def run(self, args, env=None):
        args = ['scl', 'enable', 'python27', join_args([self.path] + args)]
        return run_command(args, env=env)


class Virtualenv(object):
    def __init__(self, path, python):
        self.path = path
        self.python = python

        venv_python_path = os.path.join(self.path, 'bin/python')
        self.venv_python = python.copy_at_path(venv_python_path)

    def create(self):
        args = [
            '-m',
            'virtualenv',
            '--python',
            self.python.path,
            '--quiet',
            self.path
        ]
        env = {'PYTHONDONTWRITEBYTECODE': '1'}
        self.python.run(args, env=env)

        mkdir_p(os.path.dirname(self.venv_python.path))
        self.venv_python.create_wrapper(self.venv_python.path + '.sh')

    def run(self, args):
        return self.venv_python.run(args)

    # TODO update shebangs
    def relocate(self, python):
        python.create_wrapper(self.venv_python.path + '.sh')


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
    print join_args(args)
    return check_output(args=args, env=env, cwd=cwd)


pythons = [
    Python('/usr/bin/python2.7'),
    SCLPython('/opt/rh/python27/root/usr/bin/python2.7'),
]

python = None

for x in pythons:
    if x.exists():
        python = x
        break
else:
    raise ValueError('No python interpreter found!')

install_path = '/opt/radar-api'
install_python_path = os.path.join(install_path, 'venv/bin/python')
install_python = python.copy_at_path(install_python_path)

# Create a temporary directory to build the package in
build_path = tempfile.mkdtemp()

# Create a virtualenv
v = Virtualenv(build_path, python)
v.create()

# Install dependencies
v.run(['-m', 'pip', 'install', '-r', 'requirements.txt'])

# Install package
v.run(['-m', 'pip', 'install', '--editable', '/home/radar/src/radar'])

# Update build path references to install path
v.relocate(install_python)

# Package with fpm
# TODO

# Remove temporary directory
shutil.rmtree(build_path)
