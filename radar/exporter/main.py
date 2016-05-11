import argparse
import os

import tablib

from radar.app import create_app
from radar.exporter import exporters
from radar.exporter.config import Config
from radar.models.users import User
from radar.models.groups import Group


def get_user(value):
    try:
        user_id = int(value)
    except ValueError:
        raise argparse.ArgumentError('Not a valid user ID')

    user = User.query.get(user_id)

    if user is None:
        raise argparse.ArgumentError('User not found')

    return user


def get_group(value):
    try:
        group_id = int(value)
    except ValueError:
        raise argparse.ArgumentError('Not a valid group ID')

    group = Group.query.get(group_id)

    if group is None:
        raise argparse.ArgumentError('Group not found')

    return group


def export(name, config):
    return exporters.registry.export(name, config)


def save(data, format, dest):
    with open(dest, 'wb') as f:
        data = data.export(format)
        f.write(data)


def yn(value):
    if value == 'yes':
        return True
    elif value == 'no':
        return False
    else:
        raise argparse.ArgumentError('Must be yes or no')


if __name__ == '__main__':
    initial_parser = argparse.ArgumentParser()
    initial_parser.add_argument('--connection-string', required=True)
    initial_args, remaining_args = initial_parser.parse_known_args()

    app_config = {
        'SQLALCHEMY_DATABASE_URI': initial_args.connection_string
    }

    app = create_app(app_config)

    with app.app_context():
        # Note: xls doesn't support timezones
        formats = ['csv', 'xlsx']
        book_formats = ['xlsx']

        parser = argparse.ArgumentParser()
        parser.add_argument('--user', type=get_user)
        parser.add_argument('--patient-group', type=get_group)
        parser.add_argument('--data-group', type=get_group)
        parser.add_argument('--anonymised', action='store_true')
        parser.add_argument('--format', default='csv', choices=formats)  # TODO guess format from dest extension
        parser.add_argument('src', nargs='+')
        parser.add_argument('dest')
        args = parser.parse_args(remaining_args)

        # TODO add --source-group argument

        config = Config(
            user=args.user,
            patient_group=args.patient_group,
            data_group=args.data_group,
            anonymised=args.anonymised,
        )

        is_dir = os.path.isdir(args.dest)

        if args.format in book_formats:
            if is_dir:
                for name in args.src:
                    dest = os.path.join(args.dest, '%s.%s' % (name, args.format))
                    dataset = export(name, config)
                    dataset.title = name
                    save(dataset, args.format, dest)
            else:
                databook = tablib.Databook()

                for name in args.src:
                    dataset = export(name, config)
                    dataset.title = name
                    databook.add_sheet(dataset)

                save(databook, args.format, args.dest)
        else:
            if is_dir:
                for name in args.src:
                    dest = os.path.join(args.dest, '%s.%s' % (name, args.format))
                    dataset = export(name, config)
                    dataset.title = name
                    save(dataset, args.format, dest)
            elif len(args.src) == 1:
                name = args.src[0]
                dataset = export(name, config)
                dataset.title = name
                save(dataset, args.format, args.dest)
            else:
                parser.error('dest is not a directory')
