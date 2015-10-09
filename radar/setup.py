from setuptools import setup, find_packages

import radar

setup(
    name='radar',
    version=radar.__version__,
    long_description=radar.__doc__,
    author='UK Renal Registry',
    author_email='renalregistry@renalregistry.nhs.uk',
    url='https://www.radar.nhs.uk/',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==0.10.1',
        'Flask-SQLAlchemy==2.0',
        'itsdangerous==0.24',
        'psycopg2==2.6',
        'python-dateutil==2.4.2',
        'pytz==2015.4',
        'SQLAlchemy==1.0.8',
        'Delorean==0.5.0',
        'click==5.1',
        'six==1.9.0',
        'Jinja2==2.8'
    ],
    scripts=[
        'scripts/manage.py',
    ],
)
