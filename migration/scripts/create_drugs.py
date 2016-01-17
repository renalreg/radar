import csv

import click
from sqlalchemy import create_engine

from radar_migration import tables


def create_drugs(conn, drug_types_filename, drugs_filename):
    drug_type_map = {}

    with open(drug_types_filename) as f:
        reader = csv.reader(f)

        for row in reader:
            name = row[0]

            result = conn.execute(
                tables.drug_types.insert(),
                name=name,
            )

            drug_type_id = result.inserted_primary_key[0]

            drug_type_map[name] = drug_type_id

    with open(drugs_filename) as f:
        reader = csv.reader(f)

        for row in reader:
            drug_name, drug_type = row

            try:
                drug_type_id = drug_type_map[drug_type]
            except KeyError:
                raise ValueError('Unknown drug type: %s' % drug_type)

            conn.execute(
                tables.drugs.insert(),
                name=drug_name,
                drug_type_id=drug_type_id,
            )


@click.command()
@click.argument('db')
@click.argument('drug_types')
@click.argument('drugs')
def cli(db, drug_types, drugs):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        create_drugs(conn, drug_types, drugs)


if __name__ == '__main__':
    cli()
