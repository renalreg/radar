# RaDaR

[![Build Status](https://img.shields.io/travis/renalreg/radar/master.svg)](https://travis-ci.org/renalreg/radar) [![Code Climate](https://img.shields.io/codeclimate/github/renalreg/radar.svg)](https://codeclimate.com/github/renalreg/radar) [![Coveralls](https://img.shields.io/coveralls/renalreg/radar.svg)](https://coveralls.io/github/renalreg/radar)

## Develop

```
virtualenv venv
pip install -r dev-requirements.txt
pip install -e .
```

## Test

With tox:

```
tox
```

Or using `py.test` directly:

```
py.test radar
```

## Local Build

Install [platter](https://github.com/mitsuhiko/platter):

```
virtualenv venv
source venv/bin/activate
pip install git+https://github.com/mitsuhiko/platter
```

Build:

```
platter build -r requirements.txt .
```

This will create a `.tar.gz` file in the `dist` folder.


## Remote Build

A remote build is useful when you are developing on a different operating system to the one you want to deploy to.

Install dependencies on remote machine:

```
yum install https://download.postgresql.org/pub/repos/yum/9.4/redhat/rhel-7-x86_64/pgdg-centos94-9.4-2.noarch.rpm
yum install postgresql94 postgresql94-libs postgresql94-devel

wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py

pip install git+https://github.com/mitsuhiko/platter
```

Build:

```
fab -H $HOSTNAME -u $USER build
```

## Deploy

```
HOSTNAME=nww.radar.nhs.uk
USER=root
fab -H $HOSTNAME -u $USER deploy
```
