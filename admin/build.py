import shutil
import tempfile
import logging
import click
import os

from package import Virtualenv, run_command, relative_to_script, get_python

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RadarVirtualenv(Virtualenv):
    def install(self, src_directory, test=False):
        if test:
            # Install dev_requirements.txt
            logging.info('Installing dev_requirements.txt ...')
            self.run(
                ['-m', 'pip', 'install', '-r', 'dev_requirements.txt'],
                cwd=src_directory
            )

        # Install requirements.txt
        logging.info('Installing requirements.txt ...')
        self.run(
            ['-m', 'pip', 'install', '-r', 'requirements.txt'],
            env={'PATH': '/usr/pgsql-9.4/bin:/usr/bin:/bin'},
            cwd=src_directory
        )

        # Install radar
        logging.info('Installing radar ...')
        self.run(['setup.py', 'install'], cwd=src_directory)


def test_radar(python, src_directory, lint=True, test=True):
    logging.info('Testing ...')

    if not lint and not test:
        logging.info('Nothing to do')
        return

    tests_directory = os.path.join(src_directory, 'tests')
    test_directory = tempfile.mkdtemp()

    logging.info('Source directory is %s' % src_directory)
    logging.info('Test directory is %s' % test_directory)

    # Create the test virtualenv
    v = RadarVirtualenv(test_directory, python)
    v.create()
    v.install(src_directory, test=True)

    # Run flake8
    if lint:
        logging.info('Running flake8 ...')
        v.run(['-m', 'flake8', os.path.join(src_directory, 'radar')])

    # Run tests
    if test:
        logging.info('Running pytest ...')
        v.run(['-m', 'pytest', tests_directory])

    # Remove test directory
    logging.info('Deleting test directory ...')
    shutil.rmtree(test_directory)


def build_radar(python, src_directory, install_directory):
    build_directory = tempfile.mkdtemp()

    logging.info('Building ...')
    logging.info('Source directory is %s' % src_directory)
    logging.info('Build directory is %s' % build_directory)
    logging.info('Install directory is %s' % install_directory)

    # Create the build virtualenv
    v = RadarVirtualenv(build_directory, python)
    v.create()
    v.install(src_directory)

    # Update build path references to install path
    logging.info('Updating build virtualenv paths ...')
    v.relocate(install_directory)

    name = 'radar'
    version = python.run(['setup.py', '--version'], cwd=src_directory).strip()
    architecture = 'x86_64'
    rpm_path = '%s-%s.%s.rpm' % (name, version, architecture)

    logging.info('Version is %s' % version)

    # Package with fpm
    logging.info('Building rpm ...')
    run_command([
        'fpm',
        '-s', 'dir',
        '-t', 'rpm',
        '--package', rpm_path,
        '--name', name,
        '--version', version,
        '--url', 'http://www.radar.nhs.uk/',
        '--architecture', architecture,
        '--epoch', '0',
        '--force',
        '--depends', 'python27',
        '%s/=%s' % (build_directory, install_directory)
    ], env={'PATH': '/usr/bin:/bin'})

    # Remove build directory
    logging.info('Deleting build directory ...')
    shutil.rmtree(build_directory)

    logging.info('Successfully built rpm at %s' % rpm_path)


@click.command()
@click.option('--lint/--no-lint', default=True)
@click.option('--test/--no-test', default=True)
def main(lint, test):
    python = get_python()
    src_directory = relative_to_script('../radar')
    install_directory = '/opt/radar-api'

    test_radar(python, src_directory, lint=lint, test=test)
    build_radar(python, src_directory, install_directory)

if __name__ == '__main__':
    main()
