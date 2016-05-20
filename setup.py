from setuptools import setup, find_packages

setup(
    name='radar',
    version='2.3.13',
    description='RaDaR - Rare Disease Registry',
    author='Rupert Bedford',
    author_email='rupert.bedford@renalregistry.nhs.uk',
    url='https://www.radar.nhs.uk/',
    packages=find_packages(),
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
