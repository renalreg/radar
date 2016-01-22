import unicodecsv

from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS


class SignificantDiagnosisConverter(object):
    def __init__(self, filename):
        self.map = {}

        with open(filename, 'rb') as f:
            reader = unicodecsv.reader(f, encoding='utf-8')

            for i, row in enumerate(reader, start=1):
                old_name = row[0].upper()
                new_name = row[1].strip() or None

                if old_name in self.map:
                    print 'Duplicate disorder on line %s: %s' % (i, old_name)

                self.map[old_name] = new_name

    def convert(self, old_name):
        old_name = old_name.upper()
        new_name = self.map.get(old_name)
        return new_name


def migrate_significant_diagnoses(old_conn, new_conn, significant_diagnoses_filename):
    m = Migration(new_conn)
    sdc = SignificantDiagnosisConverter(significant_diagnoses_filename)

    rows = old_conn.execute(text("""
        SELECT
            x.radar_no,
            CASE
                WHEN x.from_date IS NOT NULL THEN
                    x.from_date
                ELSE
                    -- Use registration date if from date is missing
                    CAST(LEAST(
                        COALESCE(patient.dateReg, NOW()),
                        COALESCE(rdr_radar_number.creationDate, NOW()),
                        COALESCE(tbl_demographics.DATE_REG, NOW())
                    ) AS DATE)
            END as from_date,
            x.disorder_name
        FROM (
            (
                SELECT
                    radar_no AS radar_no,
                    date_clin_pic AS from_date,
                    sig_diag1 AS disorder_name
                FROM tbl_clinicaldata
                WHERE sig_diag1 IS NOT NULL
            )
            UNION
            (
                SELECT
                    radar_no AS radar_no,
                    date_clin_pic AS from_date,
                    sig_diag2 AS disorder_name
                FROM tbl_clinicaldata
                WHERE sig_diag2 IS NOT NULL
            )
        ) AS x
        JOIN patient ON (
            x.radar_no = patient.radarNo AND
            patient.unitcode NOT IN {0}
        )
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
    """.format(EXCLUDED_UNITS)))

    for row in rows:
        patient_id, from_date, diagnosis_name = row
        new_diagnosis_name = sdc.convert(diagnosis_name)

        if new_diagnosis_name is None:
            diagnosis_id = None
            diagnosis_text = diagnosis_name
        else:
            diagnosis_id = m.get_diagnosis_id(new_diagnosis_name)
            diagnosis_text = None

        new_conn.execute(
            tables.patient_diagnoses.insert(),
            patient_id=patient_id,
            source_group_id=m.radar_group_id,
            source_type=m.source_type,
            diagnosis_id=diagnosis_id,
            diagnosis_text=diagnosis_text,
            from_date=from_date,
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )


@click.command()
@click.argument('src')
@click.argument('dest')
@click.argument('significant_diagnoses')
def cli(src, dest, significant_diagnoses):
    src_engine = create_engine(src)
    dest_engine = create_engine(dest)

    src_conn = src_engine.connect()
    dest_conn = dest_engine.connect()

    with dest_conn.begin():
        migrate_significant_diagnoses(src_conn, dest_conn, significant_diagnoses)


if __name__ == '__main__':
    cli()
