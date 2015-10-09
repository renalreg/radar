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
        'click',
        'Delorean',
        'Flask',
        'Flask-SQLAlchemy',
        'itsdangerous',
        'Jinja2',
        'psycopg2',
        'python-dateutil',
        'pytz',
        'six',
        'SQLAlchemy',
        'Werkzeug',
    ]
)
