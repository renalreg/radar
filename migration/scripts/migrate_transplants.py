import csv

from sqlalchemy import create_engine, text
import click

from radar_migration import EXCLUDED_UNITS, tables, Migration


class ModalityConverter(object):
    modality_map = {
        '20': 20,
        '23': 23,
        '24': 24,
        '25': 25,
        '26': 26,
    }

    def __init__(self, filename):
        self.transplant_id_map = {}

        with open(filename, 'rb') as f:
            reader = csv.reader(f)

            for row in reader:
                transplant_id = int(row[0])
                modality = int(row[1])
                self.transplant_id_map[transplant_id] = modality

    def convert(self, transplant_id, old_modality):
        if transplant_id in self.transplant_id_map:
            new_modality = self.transplant_id_map[transplant_id]
        else:
            try:
                new_modality = self.modality_map[old_modality]
            except KeyError:
                raise ValueError('Unknown modality: %s' % old_modality)

        return new_modality


# TODO tbl_transplant_reject
def migrate_transplants(old_conn, new_conn, transplant_modalities_filename):
    m = Migration(new_conn)
    mc = ModalityConverter(transplant_modalities_filename)

    # TODO the recurrence dates are probably failure dates
    rows = old_conn.execute(text("""
        SELECT
            trID,
            RADAR_NO,
            DATE_TRANSPLANT,
            TRANS_TYPE,
            DATE_RECURR_TXK,
            (SELECT trFailureDate FROM tbl_transplant_reject WHERE tbl_transplant_reject.trId = tbl_transplant.trId LIMIT 1) AS DATE_FAILURE
        FROM tbl_transplant
        JOIN patient ON (
            tbl_transplant.RADAR_NO = patient.radarNo AND
            patient.unitcode NOT IN %s
        )
    """ % EXCLUDED_UNITS))

    for row in rows:
        modality = mc.convert(row['trID'], row['TRANS_TYPE'])

        new_conn.execute(
            tables.transplants.insert(),
            patient_id=row['RADAR_NO'],
            data_source_id=m.data_source_id,  # TODO
            date=row['DATE_TRANSPLANT'],
            modality=modality,
            date_of_recurrence=row['DATE_RECURR_TXK'],
            date_of_failure=row['DATE_FAILURE'],
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )


@click.command()
@click.argument('src')
@click.argument('dest')
@click.argument('transplant_modalities')
def cli(src, dest, transplant_modalities):
    src_engine = create_engine(src)
    dest_engine = create_engine(dest)

    src_conn = src_engine.connect()
    dest_conn = dest_engine.connect()

    with dest_conn.begin():
        migrate_transplants(src_conn, dest_conn, transplant_modalities)


if __name__ == '__main__':
    cli()
