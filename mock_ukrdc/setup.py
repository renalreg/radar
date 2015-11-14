import os
from setuptools import setup, find_packages

import radar_mock_ukrdc

# Hard linking doesn't work inside VirtualBox shared folders
# See: https://bitbucket.org/hpk42/tox/issues/86
if os.environ.get('USER', '') == 'vagrant':
    del os.link

setup(
    name='radar_mock_ukrdc',
    version=radar_mock_ukrdc.__version__,
    long_description=radar_mock_ukrdc.__doc__,
    author='Rupert Bedford',
    author_email='rupert.bedford@renalregistry.nhs.uk',
    url='https://www.radar.nhs.uk/',
    packages=find_packages(),
    zip_safe=True,
    install_requires=[
        'radar'
    ],
    scripts=[
        'scripts/manage.py',
    ],
)
