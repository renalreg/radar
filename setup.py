import os
from setuptools import setup, find_packages

import radar

# Hard linking doesn't work inside VirtualBox shared folders
# See: https://bitbucket.org/hpk42/tox/issues/86
if os.environ.get('USER', '') == 'vagrant':
    del os.link

setup(
    name='radar',
    version=radar.__version__,
    long_description=radar.__doc__,
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
        'delorean',  # TODO remove
        'enum34',
        'flask',
        'flask-sqlalchemy',
        'itsdangerous',
        'jinja2',
        'jsonschema',  # TODO remove
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
