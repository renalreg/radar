import tempfile
import logging
import click

from package import Virtualenv, run_command, get_python

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def install_radar(v, test=False):
    src_directory = '../radar'

    if test:
        for package_name in ['flake8', 'pytest']:
            logging.info('Installing %s ...' % package_name)
            v.install_package(package_name)

    # Install radar
    logging.info('Installing radar ...')
    v.run(['setup.py', 'install'], cwd=src_directory)


def install_api(v, test=False):
    src_directory = '../api'

    if test:
        # Install api development dependencies
        logging.info('Installing api development dependencies ...')
        v.install_requirements('../api/dev_requirements.txt')

    # Install api dependencies
    logging.info('Installing api dependencies ...')
    v.install_requirements('../api/requirements.txt', env={'PATH': '/usr/pgsql-9.4/bin:/usr/bin:/bin'})

    install_radar(v, test)

    # Install api
    logging.info('Installing api ...')
    v.run(['setup.py', 'install'], cwd=src_directory)


def test_radar(v, run_lint=True, run_tests=True):
    package_directory = '../radar/radar'
    tests_directory = '../radar/tests'

    logging.info('Testing radar ...')

    logging.info('Package directory is %s' % package_directory)
    logging.info('Tests directory is %s' % tests_directory)

    # Run flake8
    if run_lint:
        logging.info('Running flake8 ...')
        v.run(['-m', 'flake8', package_directory])

    # Run tests
    if run_tests:
        logging.info('Running pytest ...')
        v.run(['-m', 'pytest', tests_directory])


def test_api(v, run_lint=True, run_tests=True):
    test_radar(v, run_lint, run_tests)

    package_directory = '../api/radar_api'
    tests_directory = '../radar/tests'

    logging.info('Testing api ...')

    logging.info('Package directory is %s' % package_directory)
    logging.info('Tests directory is %s' % tests_directory)

    # Run flake8
    if run_lint:
        logging.info('Running flake8 ...')
        v.run(['-m', 'flake8', package_directory])

    # Run tests
    if run_tests:
        logging.info('Running pytest ...')
        v.run(['-m', 'pytest', tests_directory])


def package_api(v):
    install_directory = '/opt/radar-api'
    src_directory = '../api'

    logging.info('Packaging radar ...')
    logging.info('Install directory is %s' % install_directory)

    # Update build path references to install path
    logging.info('Updating build virtualenv paths ...')
    v.relocate(install_directory)

    name = 'radar-api'
    version = v.run(['setup.py', '--version'], cwd=src_directory).strip()
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
        '--depends', 'python',
        '%s/=%s' % (v.path, install_directory)
    ], env={'PATH': '/usr/local/bin:/usr/bin:/bin'})

    logging.info('Successfully built rpm at %s' % rpm_path)


@click.group()
def cli():
    pass


@cli.command('api')
@click.option('--run-lint/--no-lint', default=True)
@click.option('--run-tests/--no-tests', default=True)
def build_api(run_lint, run_tests):
    python = get_python()

    test = run_lint or run_tests

    if test:
        with Virtualenv(tempfile.mkdtemp(), python) as v:
            install_api(v, True)
            test_api(v, run_lint, run_tests)

    with Virtualenv(tempfile.mkdtemp(), python) as v:
        install_api(v)
        package_api(v)


@cli.command('client')
def build_web():
    pass


@cli.command('web')
def build_web():
    pass


if __name__ == '__main__':
    cli()
