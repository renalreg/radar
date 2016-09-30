import re
from setuptools import setup, find_packages

with open('radar/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

setup(
    name='radar',
    version=version,
    description='RaDaR - Rare Disease Registry',
    author='Rupert Bedford',
    author_email='rupert.bedford@renalregistry.nhs.uk',
    url='https://www.radar.nhs.uk/',
    license='AGPL-3.0',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'radar-api = radar.api.__main__:main',
            'radar-db = radar.database.__main__:main',
            'radar-exporter = radar.exporter.__main__:main',
            'radar-fixtures = radar.fixtures.__main__:main',
            'radar-ukrdc-exporter = radar.ukrdc_exporter.__main__:main',
            'radar-ukrdc-importer = radar.ukrdc_importer.__main__:main',
        ]
    },
    install_requires=[
        'backports.csv',
        'celery',
        'click',
        'cornflake',
        'enum34',
        'flask',
        'flask-admin',
        'flask-sqlalchemy',
        'inflection',
        'iso8601',
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
        'uwsgi',
        'werkzeug',
        'zxcvbn',
    ],
)
