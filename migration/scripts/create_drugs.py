import csv

import click
from sqlalchemy import create_engine

from radar_migration import tables


def create_drugs(conn, drugs_filename):
    drug_map = {}
    drugs = []

    with open(drugs_filename) as f:
        reader = csv.reader(f)

        for row in reader:
            drug_name, parent_drug_name = row

            result = conn.execute(
                tables.drugs.insert(),
                name=drug_name
            )

            drug_id = result.inserted_primary_key[0]

            drug_map[drug_name] = drug_id

            if parent_drug_name:
                drugs.append((drug_name, parent_drug_name))

    for drug_name, parent_drug_name in drugs:
        drug_id = drug_map[drug_name]
        parent_drug_id = drug_map[parent_drug_name]

        conn.execute(tables.drugs.update().where(tables.drugs.c.id == drug_id).values(parent_drug_id=parent_drug_id))


@click.command()
@click.argument('db')
@click.argument('drugs')
def cli(db, drugs):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        create_drugs(conn, drugs)


if __name__ == '__main__':
    cli()
