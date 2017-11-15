import argparse
import ConfigParser
import os

from cornflake import fields, serializers
from cornflake.sqlalchemy_orm import ReferenceField
import tablib

from radar.app import Radar
from radar.exporter.exporters import exporter_map
from radar.models.groups import Group
from radar.models.users import User


def save(data, format, dest):
    with open(dest, 'wb') as f:
        data = data.export(format)
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


def main():
    # Note: xls doesn't support timezones
    formats = ['csv', 'xlsx']
    book_formats = ['xlsx']

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('--format', default='csv', choices=formats)  # TODO guess format from dest extension
    argument_parser.add_argument('config')
    argument_parser.add_argument('dest')
    args = argument_parser.parse_args()

    app = Radar()

    config_parser = ConfigParser.ConfigParser()
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
            exporter_config = dict(
                config.items() +
                exporter_config.items()
            )
            exporter_config.update({'name': name})

            exporter = exporter_class(exporter_config)

            exporters.append((name, exporter))

        datasets = []

        # Export data
        for name, exporter in exporters:
            print('Exporting {0}...'.format(name))
            exporter.run()
            dataset = exporter.dataset
            dataset.title = name
            datasets.append(dataset)

        is_dir = os.path.isdir(args.dest)

        if args.format in book_formats:
            if is_dir:
                for dataset in datasets:
                    dest = os.path.join(args.dest, '%s.%s' % (dataset.title, args.format))
                    save(dataset, args.format, dest)
            else:
                databook = tablib.Databook()

                for dataset in datasets:
                    databook.add_sheet(dataset)

                save(databook, args.format, args.dest)
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


if __name__ == '__main__':
    main()
