import argparse
import os

import tablib

from radar.app import create_app
from radar.models.users import User
from radar.models.groups import Group

from radar_exporter.config import Config
from radar_exporter import exporters


def get_user(value):
    try:
        user_id = int(value)
    except ValueError:
        raise argparse.ArgumentError('Not a valid user ID')

    user = User.query.get(user_id)

    return user


def get_group(value):
    try:
        group_id = int(value)
    except ValueError:
        raise argparse.ArgumentError('Not a valid group ID')

    group = Group.query.get(group_id)

    return group


def export(name, config):
    return exporters.registry.export(name, config)


def save(data, format, dest):
    with open(dest, 'wb') as f:
        data = data.export(format)
        f.write(data)


if __name__ == '__main__':
    initial_parser = argparse.ArgumentParser()
    initial_parser.add_argument('--connection-string', required=True)
    initial_args, remaining_args = initial_parser.parse_known_args()

    app_config = {
        'SQLALCHEMY_DATABASE_URI': initial_args.connection_string
    }

    app = create_app(app_config)

    with app.app_context():
        formats = ['csv', 'xls', 'xlsx']
        book_formats = ['xls', 'xlsx']

        parser = argparse.ArgumentParser()
        parser.add_argument('--user', type=get_user)
        parser.add_argument('--group', type=get_group)
        parser.add_argument('--format', default='csv', choices=formats)
        parser.add_argument('src', nargs='+')
        parser.add_argument('dest')
        args = parser.parse_args(remaining_args)

        config = Config(user=args.user, group=args.group)

        is_dir = os.path.isdir(args.dest)

        if args.format in book_formats:
            if is_dir:
                for name in args.src:
                    dest = os.path.join(args.dest, '%s.%s' % (name, args.format))
                    dataset = export(name, config)
                    dataset.title = name
                    save(dataset, args.format, dest)
            else:
                databook = tablib.Dataset()

                for name in args.src:
                    dest = os.path.join(args.dest, '%s.%s' % (name, args.format))
                    dataset = export(name, config)
                    dataset.title = name
                    book.add_sheet(dataset)

                save(databook, args.format, dest)
        else:
            if is_dir:
                for name in args.src:
                    dest = os.path.join(args.dest, '%s.%s' % (name, args.format))
                    dataset = export(name, config)
                    dataset.title = name
                    save(dataset, args.format, dest)
            elif len(args.src) == 1:
                name = args.src[0]
                dest = args.dest
                dataset = export(name, config)
                dataset.title = name
                save(dataset, args.format, dest)
            else:
                parser.error('dest is not a directory')
