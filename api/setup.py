from setuptools import setup, find_packages

import radar_api

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
        'radar',
    ],
    scripts=[
        'scripts/manage.py',
    ],
)
