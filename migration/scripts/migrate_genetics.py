from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS


def migrate_genetics(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            radar_no,
            labWhereTestWasDone,
            referenceNumber,
            whatResultsShowed,
            keyEvidence,
            COALESCE(dateSent, '1900-01-01') as dateSent,
            testDoneOn
        FROM rdc_genetic_test
        JOIN patient ON (
            rdc_genetic_test.radar_no = patient.radarNo AND
            patient.unitcode NOT IN %s
        )
    """ % EXCLUDED_UNITS))

    for row in rows:
        summary = [row['testDoneOn'], row['keyEvidence']]
        summary = [x for x in summary if x]

        if summary:
            summary = '\n'.join(summary)
        else:
            summary = None

        new_conn.execute(
            tables.genetics.insert(),
            patient_id=row['radar_no'],
            cohort_id=m.cohort_id,  # TODO
            date_sent=row['dateSent'],
            laboratory=row['labWhereTestWasDone'],
            reference_number=row['referenceNumber'],
            results=row['whatResultsShowed'],
            summary=summary,
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )


@click.command()
@click.argument('src')
@click.argument('dest')
def cli(src, dest):
    src_engine = create_engine(src)
    dest_engine = create_engine(dest)

    src_conn = src_engine.connect()
    dest_conn = dest_engine.connect()

    with dest_conn.begin():
        migrate_genetics(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
