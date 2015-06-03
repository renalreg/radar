from setuptools import setup, find_packages

setup(
    name='radar',
    version='0.1',
    long_description=__doc__,
    author='Rupert Bedford',
    author_email='rupert.bedford@renalregistry.nhs.uk',
    url='https://www.renalradar.org/',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-Login',
        'Flask-Script',
        'Flask-Mail',
        'Flask-Markdown',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'itsdangerous',
        'pandas',
        'psycopg2',
        'python-dateutil',
        'pytz',
        'SQLAlchemy',
    ],
    scripts=[
        'manage.py',
    ],
)


