import csv

from pkg_resources import resource_filename

from radar_migration import tables
import radar_migration


def create_units(conn):
    filename = resource_filename(radar_migration.__name__, 'data/units.csv')
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
