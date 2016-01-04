from collections import OrderedDict

import click

from dump_tools import get_db, rows_to_csv


@click.command()
@click.argument('output', type=click.File('wb'))
@click.option('--host', default='localhost')
@click.option('--port', default=5432)
@click.option('--username', default='radar')
@click.option('--password', default='password')
@click.option('--database', default='radar')
def main(output, host, port, username, password, database):
    db = get_db('postgresql', host, port, username, password, database)
    rows = get_spec_rows(db)
    rows_to_csv(rows, output)


def get_spec_rows(db):
    rows = db.execute("""
        select
            result_group_specs.id as group_id,
            result_group_specs.code as group_code,
            result_group_specs.name as group_name,
            result_specs.id as result_id,
            result_specs.code as result_code,
            result_specs.name as result_name,
            result_specs.short_name as result_short_name,
            result_specs.type as result_type,
            result_specs.min_value as result_min_value,
            result_specs.max_value as result_max_value,
            result_specs.units as result_units,
            result_specs.min_length as result_min_length,
            result_specs.max_length as result_max_length,
            result_specs.options as result_options,
            result_specs.meta as result_meta
        from result_group_specs
        left join result_group_result_specs on result_group_result_specs.result_group_spec_id = result_group_specs.id
        left join result_specs on result_specs.id = result_group_result_specs.result_spec_id
    """)

    for row in rows:
        row = OrderedDict(row.items())

        if row['result_options'] is not None:
            row['result_options'] = OrderedDict({x['id']: x['label'] for x in row['result_options']})

        yield row


if __name__ == '__main__':
    main()
