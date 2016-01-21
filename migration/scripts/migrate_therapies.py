from sqlalchemy import create_engine, text
import click

from radar_migration import EXCLUDED_UNITS, Migration, tables


def migrate_therapies(old_conn, new_conn):
    m = Migration(new_conn)

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
            drug
        FROM (
            SELECT radar_no AS radar_no, min(date_treat) AS from_date, 'NSAID' AS drug FROM tbl_therapy
            WHERE p_nsaid = 1 OR nsaid = 1
            GROUP BY radar_no
            UNION
            SELECT radar_no, min(date_treat), 'Diuretic' FROM tbl_therapy
            WHERE p_diuretic = 1 OR diuretic = 1
            GROUP BY radar_no
            UNION
            SELECT radar_no, min(date_treat), 'Antihypertensive' FROM tbl_therapy
            WHERE p_anti_htn = 1 OR anti_htn = 1 OR p_other_anti_htn = 1 OR other_anti_htn = 1
            GROUP BY radar_no
            UNION
            SELECT radar_no, min(date_treat), 'Ace Inhibitor' FROM tbl_therapy
            WHERE p_ace_inhib = 1 OR ace_inhib = 1
            GROUP BY radar_no
            UNION
            SELECT radar_no, min(date_treat), 'Angiotension II Receptor Antogonist' FROM tbl_therapy
            WHERE p_arb_antag = 1 OR arb_antag = 1
            GROUP BY radar_no
            UNION
            SELECT radar_no, min(date_treat), 'Calcium Channel Blocker' FROM tbl_therapy
            WHERE p_ca_ch_block = 1 OR ca_ch_block = 1
            GROUP BY radar_no
            UNION
            SELECT radar_no, min(date_treat), 'Beta Blocker' FROM tbl_therapy
            WHERE p_b_block = 1 OR b_block = 1
            GROUP BY radar_no
            UNION
            SELECT radar_no, min(date_treat), 'Insulin' FROM tbl_therapy
            WHERE p_insulin = 1 OR insulin = 1
            GROUP BY radar_no
            UNION
            SELECT radar_no, min(date_treat), 'Statin' FROM tbl_therapy
            WHERE p_lip_lower_ag = 1 OR lip_lower_ag = 1
            GROUP BY radar_no
            UNION
            SELECT radar_no, min(date_treat), 'ESA (EPO)' FROM tbl_therapy
            WHERE p_epo = 1 OR epo = 1
            GROUP BY radar_no
            UNION
            SELECT radar_no, min(date_treat), 'Immunosuppressive' FROM tbl_therapy
            WHERE p_immun_sup = 1 OR immun_sup = 1 or monoclonal_yn = 1
            GROUP BY radar_no
        ) AS x
        JOIN patient ON (
            x.radar_no = patient.radarNo AND
            patient.unitcode NOT IN %s
        )
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
    """ % EXCLUDED_UNITS))

    for radar_no, from_date, drug in rows:
        drug_id = m.get_drug_id(drug)

        new_conn.execute(
            tables.medications.insert(),
            patient_id=radar_no,
            source_group_id=m.get_primary_hospital_id(radar_no),
            source_type=m.radar_source_type,
            from_date=from_date,
            drug_id=drug_id,
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )

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
            drug
        FROM (
            SELECT radar_no, from_date, drug FROM (
                SELECT radar_no AS radar_no, date_treat AS from_date, p_other_drug1 AS drug FROM tbl_therapy
                UNION
                SELECT radar_no, date_treat, p_other_drug2 FROM tbl_therapy
                UNION
                SELECT radar_no, date_treat, p_other_drug3 FROM tbl_therapy
                UNION
                SELECT radar_no, date_treat, p_other_drug4 FROM tbl_therapy
                UNION
                SELECT radar_no, date_treat, other_drug1 FROM tbl_therapy
                UNION
                SELECT radar_no, date_treat, other_drug2 FROM tbl_therapy
                UNION
                SELECT radar_no, date_treat, other_drug3 FROM tbl_therapy
                UNION
                SELECT radar_no, date_treat, other_drug4 FROM tbl_therapy
            ) AS y
            WHERE drug IS NOT NULL
            GROUP BY radar_no, drug
        ) AS x
        JOIN patient ON (
            y.radar_no = patient.radarNo AND
            patient.unitcode NOT IN %s
        )
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
    """ % EXCLUDED_UNITS))

    for radar_no, from_date, drug in rows:
        new_conn.execute(
            tables.medications.insert(),
            patient_id=radar_no,
            source_group_id=m.get_primary_hospital_id(radar_no),
            source_type=m.radar_source_type,
            from_date=from_date,
            drug_text=drug,
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
        migrate_therapies(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
