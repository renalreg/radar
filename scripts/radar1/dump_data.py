#!/usr/bin/env python

from collections import defaultdict, OrderedDict
import os.path

import click
from sqlalchemy import create_engine

from dump_tools import rows_to_csv


@click.command()
@click.argument('src')
@click.argument('dest', default='.')
def main(src, dest):
    engine = create_engine(src)
    conn = engine.connect()

    tables = get_tables(conn)
    tables_to_csv(conn, tables, dest)


def get_tables(conn):
    """Gets a list of tables and their columns."""

    columns = conn.execute("""
        select
            table_name,
            column_name
        from information_schema.columns
        where
            table_schema = DATABASE() and
            (
                table_name = 'diagnosis' or
                table_name = 'medicine' or
                table_name = 'patient' or
                table_name like 'rdc_%%' or
                table_name like 'rdr_%%' or
                table_name like 'tbl_%%' or
                table_name = 'testresult' or
                table_name = 'unit' or
                table_name = 'user' or
                table_name = 'usermapping'
            )
        order by table_name, ordinal_position
    """)

    tables = defaultdict(list)

    for column in columns:
        table_name = column['table_name']
        column_name = column['column_name']
        tables[table_name].append(column_name)

    tables = OrderedDict(sorted(tables.items()))

    return tables


def tables_to_csv(conn, tables, output_dir):
    """Dumps the data in each table to a CSV file in the output directory."""

    for table_name, column_names in tables.items():
        print table_name
        output_filename = os.path.join(output_dir, table_name + '.csv')
        output_file = open(output_filename, 'wb')
        table_to_csv(conn, table_name, column_names, output_file)


def table_to_csv(conn, table_name, column_names, output_file):
    """Dump a table to a CSV file."""

    rows = get_data(conn, table_name, column_names)
    rows_to_csv(rows, output_file)


def get_data(conn, table_name, column_names):
    columns = ','.join('`%s`' % x for x in column_names)
    return conn.execute('select {columns} from {table_name} limit 100000'.format(
        table_name=table_name,
        columns=columns
    ))


if __name__ == '__main__':
    main()
