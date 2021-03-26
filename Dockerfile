FROM python:3.6

WORKDIR /radar

COPY . /radar

RUN pip install --upgrade pip

RUN pip install -r dev-requirements.txt

RUN pip install -e .

ENV RADAR_SETTINGS /radar/example_settings.py

ENV FLASK_ENV development



