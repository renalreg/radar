FROM centos:7 AS dev

WORKDIR /radar

RUN yum update -y && yum install -y https://centos7.iuscommunity.org/ius-release.rpm epel-release

# Install Python 3.6 and upgrade tools

RUN yum install -y python36 python36-pip python36-devel libpqxx-devel.x86_64 pcre-devel

RUN python3 -m pip install --upgrade pip setuptools==57.5.0 wheel

RUN yum -y install python-pip

# Dev tools

RUN yum clean all && yum groupinstall -y "Development Tools"

# Install Radar

COPY . /radar

RUN python3 -m pip install -r dev-requirements.txt && python3 -m pip install -e .

# Create a venv for building deployemnt packages

RUN python3 -m virtualenv -p python2 venv

RUN source ./venv/bin/activate && pip install --upgrade pip==20.3.4 setuptools==44.1.1 wheel==0.36.2

RUN source ./venv/bin/activate && pip install platter

# Enviroment variables

ENV RADAR_SETTINGS /radar/example_settings.py

ENV FLASK_ENV development

# Set locales :- See https://click.palletsprojects.com/en/7.x/python3/

ENV LC_ALL=en_US.utf8

ENV LANG=en_US.utf8

# Build for production stage

RUN source ./venv/bin/activate && platter build --virtualenv-version 15.1.0 -p python3 -r requirements.txt .

# Production Image

FROM centos:7 AS prod

COPY --from=dev /radar/dist/ /srv/radar/

RUN yum update -y && yum install -y https://centos7.iuscommunity.org/ius-release.rpm epel-release

# Install Python 3.6 and upgrade tools

RUN yum install -y python36 python36-pip python36-devel libpqxx-devel.x86_64

RUN tar -xzf /srv/radar/radar* -C /srv/radar/ && rm -rf /srv/radar/radar*.tar.gz && mkdir /srv/radar/current

RUN /srv/radar/radar*/install.sh /srv/radar/current/ && rm -rf /srv/radar/radar*

RUN useradd -ms /bin/bash radar
