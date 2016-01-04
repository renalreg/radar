import csv

from radar_migration import tables


ORGANISATIONS = [
    ('NHS', 'NHS', True),
    ('CHI', 'CHI', True),
    ('UKRR', 'UK Renal Registry', True),
    ('HANDC', 'H&C', True),
    ('UKRDC', 'UKRDC', True),
    ('NHSBT', 'NHS Blood and Transplant', True),
    ('BAPN', 'BAPN', True),
]


def create_organisations(conn):
    for code, name, recruitment in ORGANISATIONS:
        conn.execute(
            tables.organisations.insert(),
            code=code,
            type='OTHER',
            name=name,
            recruitment=recruitment,
        )


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
