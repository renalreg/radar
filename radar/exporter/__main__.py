import argparse
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import os
import socket
import sqlite3

from cornflake import fields, serializers
from cornflake.sqlalchemy_orm import ReferenceField
import tablib

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


def main():
    # Note: xls doesn't support timezones
    formats = ['csv', 'xlsx', 'sqlite']
    book_formats = ['xlsx']

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('--format', default='csv', choices=formats)  # TODO guess format from dest extension
    argument_parser.add_argument('config')
    argument_parser.add_argument('dest')
    args = argument_parser.parse_args()

    app = Radar()

    config_parser = ConfigParser()
    config_parser.readfp(open(args.config))

    with app.app_context():
        config = parse_config(config_parser)

        exporters = []

        # Create exporters
        for name in config_parser.sections():
            if name == 'global':
                continue

            exporter_class = exporter_map[name]

            data = dict(config_parser.items(name))
            exporter_config = exporter_class.parse_config(data)

            exporter_config.update(config)
            exporter_config.update({'name': name})

            exporter = exporter_class(exporter_config)

            exporters.append((name, exporter))

        datasets = []
        error = False

        is_dir = os.path.isdir(args.dest)

        if args.format == 'sqlite':
            # NOTE: This will crash if the file already exists
            # Annoyingly only after its finished querying
            connection = sqlite3.connect(args.dest)
            cursor = connection.cursor()

        # Export data
        for name, exporter in exporters:
            print('Exporting {0}...'.format(name))
            exporter.run()
            dataset = exporter.dataset
            if name == 'nurtureckd':
                name = 'visits'
            dataset.title = name
            datasets.append(dataset)

            if args.format == 'sqlite':

                print('Saving to SQLite {0}...'.format(name))

                # Change so SQLite is happy as a table name
                name = name.replace("-", "_")
                name = name.replace(" ", "_")
                name = name.replace(":", "_")
                name = name.replace(">", "_")

                resultset = exporter.plain_rows

                sqlstring = exporter.get_create_table_string(name)
                try:
                    cursor.execute(sqlstring)
                except:
                    print(exporter._columns)
                    print(sqlstring)
                    raise

                sqlstring = exporter.get_insert_string(name)

                for insert_row in resultset:
                    try:
                        cursor.execute(sqlstring, insert_row)
                    except Exception:
                        print(exporter._columns)
                        print(sqlstring)
                        print(insert_row)
                        raise

                    connection.commit()

        if args.format in book_formats:

            if is_dir:
                for dataset in datasets:
                    dest = os.path.join(args.dest, '%s.%s' % (dataset.title, args.format))
                    save(dataset, args.format, dest, binary=True)
            else:
                databook = tablib.Databook()

                for dataset in datasets:
                    databook.add_sheet(dataset)

                save(databook, args.format, args.dest, binary=True)
        else:
            if is_dir:
                for dataset in datasets:
                    dest = os.path.join(args.dest, '%s.%s' % (dataset.title, args.format))
                    save(dataset, args.format, dest)
            elif len(datasets) == 1:
                save(datasets[0], args.format, args.dest)
            elif len(datasets):
                # TODO raise this error earlier
                argument_parser.error('dest is not a directory')
                error = True

        if not error:
            log_data_export(config, config_parser.sections())


if __name__ == '__main__':
    main()
