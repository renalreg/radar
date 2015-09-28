from setuptools import setup, find_packages

setup(
    name='radar',
    version='0.2.0',
    long_description=__doc__,
    author='Rupert Bedford',
    author_email='rupert.bedford@renalregistry.nhs.uk',
    url='https://www.renalradar.org/',
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
