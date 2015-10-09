import os
from setuptools import setup, find_packages

import radar_api

# Hard linking doesn't work inside VirtualBox shared folders
# See: https://bitbucket.org/hpk42/tox/issues/86
if os.environ.get('USER', '') == 'vagrant':
    del os.link

setup(
    name='radar_api',
    version=radar_api.__version__,
    long_description=radar_api.__doc__,
    author='UK Renal Registry',
    author_email='renalregistry@renalregistry.nhs.uk',
    url='https://www.radar.nhs.uk/',
    packages=find_packages(),
    zip_safe=True,
    install_requires=[
        'Flask',
        'radar',
        'six',
        'SQLAlchemy',
    ],
    scripts=[
        'scripts/manage.py',
    ],
)
