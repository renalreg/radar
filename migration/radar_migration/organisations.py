import csv

from radar_migration import tables


def create_units(conn, filename):
    f = open(filename, 'rb')
    reader = csv.reader(f)

    for row in reader:
        conn.execute(
            tables.organisations.insert(),
            code=row[0],
            type='UNIT',
            name=row[1],
            recruitment=False,
        )

    f.close()
