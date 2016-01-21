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


def migrate_transplants(old_conn, new_conn, transplant_modalities_filename):
    m = Migration(new_conn)
    mc = ModalityConverter(transplant_modalities_filename)

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

        result = new_conn.execute(
            tables.transplants.insert(),
            patient_id=row['RADAR_NO'],
            source_group_id=m.radar_group_id,  # TODO
            source_type=m.source_type,
            date=row['DATE_TRANSPLANT'],
            modality=modality,
            date_of_recurrence=row['DATE_RECURR_TXK'],
            date_of_failure=row['DATE_FAILURE'],
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )

        old_transplant_id = row['trID']
        transplant_id = result.inserted_primary_key[0]

        rejections = old_conn.execute(
            text("""
                SELECT DISTINCT
                    trRejectDate
                FROM tbl_transplant_reject
                WHERE
                    trID = :old_transplant_id AND
                    trRejectDate IS NOT NULL
            """),
            old_transplant_id=old_transplant_id,
        )

        for rejection in rejections:
            new_conn.execute(
                tables.transplant_rejections.insert(),
                transplant_id=transplant_id,
                date_of_rejection=rejection['trRejectDate'],
            )

        biopsies = old_conn.execute(
            text("""
                SELECT DISTINCT
                    trBiopsyDate,
                    tbl_transplant.TRANS_RECURR
                FROM tbl_transplant_reject
                JOIN tbl_transplant ON tbl_transplant_reject.trID = tbl_transplant.trID
                WHERE
                    tbl_transplant_reject.trID = :old_transplant_id AND
                    trBiopsyDate IS NOT NULL
            """),
            old_transplant_id=old_transplant_id,
        )

        for biopsy in biopsies:
            new_conn.execute(
                tables.transplant_biopsies.insert(),
                transplant_id=transplant_id,
                date_of_biopsy=biopsy['trBiopsyDate'],
                recurrence=biopsy['TRANS_RECURR'] == '\1',
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
