import os
from setuptools import setup, find_packages

__version__ = '2.3.0'

# Hard linking doesn't work inside VirtualBox shared folders
# See: https://bitbucket.org/hpk42/tox/issues/86
if os.environ.get('USER', '') == 'vagrant':
    del os.link

setup(
    name='radar',
    version=__version__,
    long_description=__doc__,
    author='Rupert Bedford',
    author_email='rupert.bedford@renalregistry.nhs.uk',
    url='https://www.radar.nhs.uk/',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'celery',
        'click',
        'cornflake',
        'enum34',
        'flask',
        'flask-sqlalchemy',
        'itsdangerous',
        'jinja2',
        'librabbitmq',
        'psycopg2',
        'python-dateutil',
        'pytz',
        'requests',
        'six',
        'sqlalchemy',
        'sqlalchemy-enum34',
        'termcolor',
        'werkzeug',
        'zxcvbn',
    ],
)
