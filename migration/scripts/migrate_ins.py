import csv

from sqlalchemy import create_engine, text
import click

from radar_migration import Migration, tables, EXCLUDED_UNITS, bit_to_bool

KIDNEY_TYPE_MAP = {
    None: None,
    '\0': 'NATIVE',
    '\1': 'TRANSPLANT',
}

REMISSION_TYPE_MAP = {
    None: None,
    1: 'COMPLETE',
    2: 'PARTIAL',
    3: 'NONE',
    9: None,
}


def convert_kidney_type(old_value):
    try:
        new_value = KIDNEY_TYPE_MAP[old_value]
    except KeyError:
        raise ValueError('Unknown kidney type: %s' % old_value)

    return new_value


def convert_remission_type(old_value):
    try:
        new_value = REMISSION_TYPE_MAP[old_value]
    except KeyError:
        raise ValueError('Unknown remission type: %s' % old_value)

    return new_value


class DrugConverter(object):
    def __init__(self, filename):
        self.map = {}
        self.high_dose_oral_prednisolone = set()
        self.iv_methyl_prednisolone = set()

        with open(filename, 'rb') as f:
            reader = csv.reader(f)

            for row in reader:
                old_drug = row[0].lower()
                field = int(row[1])
                new_drug = row[2] or None

                if field == 1:
                    self.high_dose_oral_prednisolone.add(old_drug)
                elif field == 2:
                    self.iv_methyl_prednisolone.add(old_drug)

                if old_drug in self.map:
                    raise ValueError('Duplicate drug: %s' % old_drug)

                self.map[old_drug] = new_drug

    def convert_iv_methyl_prednisolone(self, old_drugs):
        if any(old_drugs):
            r = any(x and x.lower() in self.iv_methyl_prednisolone for x in old_drugs)
        else:
            r = None

        return r

    def convert_high_dose_oral_prednisolone(self, old_drugs):
        if any(old_drugs):
            r = any(x and x.lower() in self.high_dose_oral_prednisolone for x in old_drugs)
        else:
            r = None

        return r

    def convert_drugs(self, old_drugs):
        new_drugs = []

        for old_drug in old_drugs:
            if old_drug is None:
                continue

            old_drug = old_drug.lower()

            try:
                new_drug = self.map[old_drug]
            except KeyError:
                raise ValueError('Unknown drug: %s' % old_drug)

            if new_drug is not None:
                new_drugs.append(new_drug)

        return new_drugs


def migrate_ins_relapses(old_conn, new_conn, ins_relapse_drugs_filename):
    m = Migration(new_conn)
    dc = DrugConverter(ins_relapse_drugs_filename)

    rows = old_conn.execute(text("""
        SELECT
            RADAR_NO,
            DATE_ONSET_RELAP,
            RELAP_TX_NAT,
            TRIG_VIRAL,
            TRIG_IMMUN,
            TRIG_OTHER,
            REMISS_ACHIEVE,
            DATE_REMISSION,
            RELAP_DRUG_1,
            RELAP_DRUG_2,
            RELAP_DRUG_3
        FROM tbl_relapse
        JOIN patient ON (
            tbl_relapse.radar_no = patient.radarNo AND
            patient.unitcode NOT IN %s
        )
    """ % EXCLUDED_UNITS))

    for row in rows:
        kidney_type = convert_kidney_type(row['RELAP_TX_NAT'])
        remission_type = convert_remission_type(row['REMISS_ACHIEVE'])

        old_drugs = [row['RELAP_DRUG_1'], row['RELAP_DRUG_2'], row['RELAP_DRUG_3']]
        high_dose_oral_prednisolone = dc.convert_high_dose_oral_prednisolone(old_drugs)
        iv_methyl_prednisolone = dc.convert_iv_methyl_prednisolone(old_drugs)

        new_conn.execute(
            tables.ins_relapses.insert(),
            patient_id=row['RADAR_NO'],
            date_of_relapse=row['DATE_ONSET_RELAP'],
            kidney_type=kidney_type,
            viral_trigger=row['TRIG_VIRAL'],
            immunisation_trigger=row['TRIG_IMMUN'],
            other_trigger=row['TRIG_OTHER'],
            high_dose_oral_prednisolone=high_dose_oral_prednisolone,
            iv_methyl_prednisolone=iv_methyl_prednisolone,
            date_of_remission=row['DATE_REMISSION'],
            remission_type=remission_type,
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )

        new_drugs = dc.convert_drugs(old_drugs)

        for new_drug in new_drugs:
            drug_id = m.get_drug_id(new_drug)

            new_conn.execute(
                tables.medications.insert(),
                patient_id=row['RADAR_NO'],
                source_group_id=m.group_id,  # TODO
                source_type=m.source_type,
                from_date=row['DATE_ONSET_RELAP'],
                drug_id=drug_id,
                created_user_id=m.user_id,
                modified_user_id=m.user_id,
            )


def migrate_ins_clinical_pictures(old_conn, new_conn):
    m = Migration(new_conn)

    rows = old_conn.execute(text("""
        SELECT
            tbl_clinicaldata.RADAR_NO,
            CASE
                WHEN DATE_CLIN_PIC IS NOT NULL AND DATE_CLIN_PIC != '0000-00-00 00:00:00' THEN
                    DATE_CLIN_PIC
                ELSE
                    -- Use registration date if result date is missing
                    CAST(LEAST(
                        COALESCE(patient.dateReg, NOW()),
                        COALESCE(rdr_radar_number.creationDate, NOW()),
                        COALESCE(tbl_demographics.DATE_REG, NOW())
                    ) AS DATE)
            END as DATE_CLIN_PIC,
            INFECTION,
            INFECTION_DETAIL,
            THROMBOSIS,
            PERITONITIS,
            PUL_OED,
            RASH,
            RASH_DETAIL,
            HYPOVAL,
            FEVER,
            HTH_REQ_TMT,
            tbl_clinicaldata.COMMENTS,
            OPTHALM,
            OPTHALM_DETAIL,
            OEDEMA,
            PREC_INF,
            PREC_INF_DETAIL
        FROM tbl_clinicaldata
        JOIN patient ON (
            tbl_clinicaldata.radar_no = patient.radarNo AND
            patient.unitcode NOT IN {0}
        )
        LEFT JOIN rdr_radar_number ON patient.radarNo = rdr_radar_number.id
        LEFT JOIN tbl_demographics ON patient.radarNo = tbl_demographics.radar_no
        WHERE
            -- Only SRNS (INS) patients
            EXISTS (
                SELECT 1 FROM usermapping
                WHERE
                    usermapping.nhsno = patient.nhsno AND
                    usermapping.unitcode = 'SRNS'
            )
    """.format(EXCLUDED_UNITS)))

    for row in rows:
        patient_id = row['RADAR_NO']
        date_of_picture = row['DATE_CLIN_PIC']
        oedema = bit_to_bool(row['OEDEMA'])
        hypovalaemia = bit_to_bool(row['HYPOVAL'])
        fever = bit_to_bool(row['FEVER'])
        thrombosis = bit_to_bool(row['THROMBOSIS'])
        peritonitis = bit_to_bool(row['PERITONITIS'])
        pulmonary_odemea = bit_to_bool(row['PUL_OED'])
        hypertension = bit_to_bool(row['HTH_REQ_TMT'])
        rash = bit_to_bool(row['RASH'])
        rash_details = row['RASH_DETAIL']
        infection = bit_to_bool(row['PREC_INF'])
        infection_details = row['PREC_INF_DETAIL']
        ophthalmoscopy = bit_to_bool(row['OPTHALM'])
        ophthalmoscopy_details = row['OPTHALM_DETAIL']
        comments = row['COMMENTS']

        new_conn.execute(
            tables.ins_clinical_pictures.insert(),
            patient_id=patient_id,
            date_of_picture=date_of_picture,
            oedema=oedema,
            hypovalaemia=hypovalaemia,
            fever=fever,
            thrombosis=thrombosis,
            peritonitis=peritonitis,
            pulmonary_odemea=pulmonary_odemea,
            hypertension=hypertension,
            rash=rash,
            rash_details=rash_details,
            infection=infection,
            infection_details=infection_details,
            ophthalmoscopy=ophthalmoscopy,
            ophthalmoscopy_details=ophthalmoscopy_details,
            comments=comments,
            created_user_id=m.user_id,
            modified_user_id=m.user_id,
        )


@click.command()
@click.argument('src')
@click.argument('dest')
@click.argument('ins_relapse_drugs')
def cli(src, dest, ins_relapse_drugs):
    src_engine = create_engine(src)
    dest_engine = create_engine(dest)

    src_conn = src_engine.connect()
    dest_conn = dest_engine.connect()

    with dest_conn.begin():
        migrate_ins_relapses(src_conn, dest_conn, ins_relapse_drugs)
        migrate_ins_clinical_pictures(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
