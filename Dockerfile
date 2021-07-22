FROM centos:7

WORKDIR /radar

RUN yum update -y

RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm epel-release

# Install Python 3.6 and upgrade tools

RUN yum install -y python36 python36-pip python36-devel libpqxx-devel.x86_64 python-devel

RUN python3 -m pip install --upgrade pip setuptools wheel

RUN yum -y install python-pip

# Dev tools

RUN yum clean all

RUN yum groupinstall -y "Development Tools"

# Install Radar

COPY . /radar

RUN python3 -m pip install -r dev-requirements.txt

RUN python3 -m pip install -e .

# Create a venv for building deployemnt packages

# RUN python3 -m virtualenv -p python2 venv

# RUN source ./venv/bin/activate && pip install --upgrade pip==20.3.4 setuptools==44.1.1 wheel==0.36.2

# RUN source ./venv/bin/activate && pip install platter

# Enviroment variables

ENV RADAR_SETTINGS /radar/bch_settings.py

ENV FLASK_ENV development

# Set locales :- See https://click.palletsprojects.com/en/7.x/python3/

ENV LC_ALL=en_US.utf8

ENV LANG=en_US.utf8

