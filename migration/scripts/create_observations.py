import csv

import click
from sqlalchemy import create_engine

from radar_migration import tables


def optional_float(old_value):
    if old_value:
        new_value = float(old_value)
    else:
        new_value = None

    return new_value


def create_observations(conn, observations_filename):
    with open(observations_filename, 'rb') as f:
        reader = csv.reader(f)

        for row in reader:
            row = [x or None for x in row]
            name = row[0]
            short_name = row[1]
            value_type = row[2]
            sample_type = row[3]
            units = row[4]
            min_value = optional_float(row[5])
            max_value = optional_float(row[6])
            min_length = min_value
            max_length = max_value
            options = row[7]
            pv_code = row[8]

            properties = {}

            if value_type == 'INTEGER' or value_type == 'REAL':
                if min_value is None:
                    min_value = 0

                properties['min_value'] = min_value

                if max_value is not None:
                    properties['max_value'] = max_value

                if units is not None:
                    properties['units'] = units
            elif value_type == 'ENUM':
                properties['options'] = []

                for option in options.split(','):
                    parts = option.split('-', 2)
                    parts = [x.strip() for x in parts]
                    code, description = parts
                    properties['options'].append({'code': code, 'description': description})
            elif value_type == 'STRING':
                if min_length is None:
                    min_length = 0

                properties['min_length'] = min_length

                if max_length is not None:
                    properties['max_length'] = max_length

            conn.execute(
                tables.observations.insert(),
                name=name,
                short_name=short_name,
                value_type=value_type,
                sample_type=sample_type,
                pv_code=pv_code,
                properties=properties,
            )


@click.command()
@click.argument('db')
@click.argument('observations')
def cli(db, observations):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        create_observations(conn, observations)


if __name__ == '__main__':
    cli()
