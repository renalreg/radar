import argparse
from configparser import ConfigParser
import csv
from datetime import date
import io
import os
import shutil
import socket
import tempfile

from cornflake import fields, serializers
from cornflake.sqlalchemy_orm import ReferenceField

from radar.app import Radar
from radar.database import db
from radar.exporter.exporters import exporter_map
from radar.models.groups import Group
from radar.models.logs import Log
from radar.models.users import User


def save(data, format, dest, binary=False):

    data = data.export(format)

    if not binary:
        try:
            data = data.decode('utf-8')
        except Exception:
            pass

        data = data.encode('utf-8')

    with open(dest, 'wb') as f:
        f.write(data)


class GroupField(ReferenceField):
    model_class = Group


class UserField(ReferenceField):
    model_class = User


class ConfigSerializer(serializers.Serializer):
    anonymised = fields.BooleanField(required=False)
    data_group = GroupField(required=False)
    patient_group = GroupField(required=False)
    user = UserField(required=False)


def parse_config(config_parser):
    if config_parser.has_section('global'):
        data = dict(config_parser.items('global'))
    else:
        data = dict()

    serializer = ConfigSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    return validated_data


def log_data_export(config, sections):
    if 'global' in sections:
        sections.remove('global')

    data = {'hostname': socket.getfqdn()}
    if config.get('patient_group'):
        data['patient_group'] = config['patient_group'].id
    if config.get('data_group'):
        data['data_group'] = config['data_group'].id
    if config.get('anonymised'):
        data['anonymised'] = config.get('anonymised')
    if config.get('user'):
        data['user'] = config.get('user')

    data['exporters'] = sections

    log = Log()
    log.type = 'DATA_EXPORTER'
    log.data = data
    db.session.add(log)
    db.session.commit()


class TemporaryDirectory(object):
    """
    Context manager for mkdtemp, as TemporaryDirectory is not
    available in python2, only python>3.2
    """
    def __init__(self, prefix):
        self.prefix = prefix
        self.name = tempfile.mkdtemp(self.prefix)

    def __enter__(self):
        return self.name

    def __exit__(self, exc, value, tb):
        shutil.rmtree(self.name, ignore_errors=True)


def main():

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('config')
    argument_parser.add_argument('dest')
    args = argument_parser.parse_args()

    app = Radar()

    config_parser = ConfigParser()
    config_parser.readfp(open(args.config))

    with app.app_context(), TemporaryDirectory(prefix='rdrexp') as output:
        config = parse_config(config_parser)

        exporters = []

        # Create exporters
        for name in config_parser.sections():
            if name == 'global':
                continue

            exporter_class = exporter_map[name]

            # make a copy of config
            exporter_config = dict(**config)
            exporter_config.update({'name': name})

            exporter = exporter_class(exporter_config)

            exporters.append((name, exporter))

        # Export data
        for name, exporter in exporters:
            print('Exporting {0}...'.format(name))
            if name == 'nurtureckd':
                name = 'visits'

            fname = os.path.join(output, '{}.csv'.format(name))

            exporter.setup()
            with io.open(fname, 'w', encoding='utf-8', newline='') as openfd:
                writer = csv.writer(openfd)
                for row in exporter.get_rows():
                    writer.writerow(row)

        group_name = config['patient_group'].code.lower()
        today = date.today().strftime('%Y-%m-%d')
        anon = ''
        if config['anonymised']:
            anon = '-anon'
        archive_name = '{}-export-{}{}'.format(today, group_name, anon)
        shutil.make_archive(os.path.join(args.dest, archive_name), 'zip', output)

        log_data_export(config, config_parser.sections())


if __name__ == '__main__':
    main()
