from sqlalchemy import text, create_engine
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS


OBSERVATIONS = [
    ('Creatinine', 'creat_ser'),
    ('PROTEIN', 'protein'),
    ('Alb', 'albumin'),
    ('Urea', 'urea_ser'),
    ('Sodium', 'sodium'),
    ('Potassium', 'potassium'),
    ('Phos', 'phos'),
    ('PCR', 'prot_creat_rat'),
    ('ACR', 'alb_creat_rat'),
    ('WBC', 'wbc'),
    ('Hb', 'hb'),
    ('NEUTRO', 'neutro'),
    ('Plats', 'platelets'),
    ('Ferr', 'ferritin'),
    ('Cholest', 'chol_total'),
    ('hdl', 'chol_hdl'),
    ('ldl', 'chol_ldl'),
    ('TG', 'trig'),
    ('CCL', 'creat_clear_schz'),
    ('t4', 'thyrox'),
    ('tsh', 'tsh'),
    ('ANCA', 'anca'),
    ('ENA', 'ena'),
    ('ANA', 'ana'),
    ('Anti_dsDNA', 'dna_anti_ds'),
    ('Cryoglob', 'cryoglob'),
    ('Anti_GBM', 'anti_gbm'),
    ('IGG', 'igg'),
    ('IGA', 'iga'),
    ('IGM', 'igm'),
    ('Comp_C3', 'comp_c3'),
    ('Comp_C4', 'comp_c4'),
    ('C3_Neph', 'c3_neph_fac'),
    ('INR', 'inr'),
    ('CRP', 'crp'),
    ('Anti_Strep', 'anti_strep_o'),
    ('HBV', 'hep_b'),
    ('HCV', 'hep_c'),
    ('HIV', 'hiv'),
    ('EBV', 'ebv'),
    ('CMV', 'cmv'),
    ('Parvo', 'parvo_antib'),
    ('UVOL24', 'ur_vol_24h'),
    ('UDHAEM', 'haematuria'),
    ('UDRC', 'dys_eryth_urine'),
    ('URC', 'red_ccasts_urine'),
    ('UDLEUC', 'leuc_urine'),
    ('UDNIT', 'nitrite'),
    ('UBACT', 'bact_urine'),
    ('UDGLUC', 'gluc_urine'),
    ('UOSMOLAL', 'osmolarity'),
    ('UDPROT', 'proteinuria_dip'),
    ('Anti_c1q', 'ANTI_CLQ'),
]

TEMPLATE = """
    SELECT
        radar_no as radar_no,
        date_lab_res as result_date,
        '{0}' as result_code,
        {1} as result_value
    FROM tbl_labdata
"""


def migrate_radar_results(old_conn, new_conn):
    m = Migration(new_conn)

    q = '\nUNION\n'.join(TEMPLATE.format(*x) for x in OBSERVATIONS)

    q = """
        SELECT * FROM ({0}) AS results
        JOIN patient ON (
            results.radar_no = patient.radarNo AND
            patient.unitcode NOT IN {1}
        )
        WHERE result_date IS NOT NULL AND result_value IS NOT NULL
    """.format(q, EXCLUDED_UNITS)

    rows = old_conn.execute(text(q))

    for i, row in enumerate(rows):
        if i % 10000 == 0:
            print i

        patient_id = row[0]
        result_date = row[1]
        observation_short_name = row[2]
        result_value = row[3]
        observation_id = m.get_observation_id(short_name=observation_short_name)

        new_conn.execute(
            tables.results.insert(),
            patient_id=patient_id,
            source_group_id=m.group_id,
            source_type=m.source_type,
            observation_id=observation_id,
            date=result_date,
            value=result_value,
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
        migrate_radar_results(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
