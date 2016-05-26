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
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'radar-exporter = radar.exporter.__main__:main',
            'radar-ukrdc-exporter = radar.ukrdc_exporter.__main__:main',
        ]
    },
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
        'uwsgi',
        'werkzeug',
        'zxcvbn',
    ],
)
