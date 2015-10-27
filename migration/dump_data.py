#!/usr/bin/env python

from collections import defaultdict, OrderedDict
from datetime import date, datetime
import csv
import os.path

from sqlalchemy import create_engine
import click


@click.command()
@click.argument('output_dir', default='.')
@click.option('--host', default='localhost')
@click.option('--port', default=3306)
@click.option('--username', default='dbaccess')
@click.option('--password', required=True)
@click.option('--database', default='patientview')
def main(output_dir, host, port, username, password, database):
    db = get_db('mysql', host, port, username, password, database)
    tables = get_tables(db, database)
    tables_to_csv(db, tables, output_dir)


def get_db(schema, host, port, username, password, database):
    connection_string = '{schema}://{username}:{password}@{host}:{port}/{database}'.format(
        schema=schema,
        host=host,
        port=port,
        username=username,
        password=password,
        database=database,
    )
    db = create_engine(connection_string)
    return db


def get_tables(db, database_name):
    """Gets a list of tables and their columns."""

    columns = db.execute("""
        select
            table_name,
            column_name
        from information_schema.columns
        where
            table_schema = %s and
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
    """, [database_name])

    tables = defaultdict(list)

    for column in columns:
        table_name = column['table_name']
        column_name = column['column_name']
        tables[table_name].append(column_name)

    tables = OrderedDict(sorted(tables.items()))

    return tables


def tables_to_csv(db, tables, output_dir):
    """Dumps the data in each table to a CSV file in the output directory."""

    for table_name, column_names in tables.items():
        print table_name
        output_filename = os.path.join(output_dir, table_name + '.csv')
        output_file = open(output_filename, 'wb')
        table_to_csv(db, table_name, column_names, output_file)


def table_to_csv(db, table_name, column_names, output_file):
    """Dump a table to a CSV file."""

    writer = csv.writer(output_file)

    writer.writerow(column_names)

    rows = get_data(db, table_name, column_names)

    for row in rows:
        writer.writerow([to_str(x) for x in row])


def get_data(db, table_name, column_names):
    columns = ','.join('`%s`' % x for x in column_names)
    return db.execute('select {columns} from {table_name} limit 100000'.format(
        table_name=table_name,
        columns=columns
    ))


def to_str(value):
    if isinstance(value, date):
        value = date_to_str(value)
    elif isinstance(value, datetime):
        value = datetime_to_str(value)

    return value


def date_to_str(value):
    return '%04d-%02d-%02d' % (
        value.year,
        value.month,
        value.day,
    )


def datetime_to_str(value):
    return '%04d-%02d-%02d %02d:%02d:%02d' % (
        value.year,
        value.month,
        value.day,
        value.hour,
        value.minute,
        value.second,
    )


if __name__ == '__main__':
    main()
