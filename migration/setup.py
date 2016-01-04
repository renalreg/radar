import os
from setuptools import setup, find_packages

import radar_migration

# Hard linking doesn't work inside VirtualBox shared folders
# See: https://bitbucket.org/hpk42/tox/issues/86
if os.environ.get('USER', '') == 'vagrant':
    del os.link

setup(
    name='radar-migration',
    version=radar_migration.__version__,
    long_description=radar_migration.__doc__,
    author='Rupert Bedford',
    author_email='rupert.bedford@renalregistry.nhs.uk',
    url='https://www.radar.nhs.uk/',
    packages=find_packages(),
    zip_safe=True,
    scripts=[
        'scripts/migrate.py',
    ],
)
