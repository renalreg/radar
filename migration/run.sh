#!/bin/sh

set -e

usage() {
  echo "Usage: $0 mysql+pymysql://radar:password@10.0.2.2:3306/radar?charset=utf8 postgresql+psycopg2://postgres:password@localhost:5432/radar"
  exit 1
}

if [ "$#" -ne 2 ]; then
  usage
fi

SRC=$1
DEST=$2

echo 'create users...'
python scripts/create_users.py "$DEST"
echo 'create cohorts...'
python scripts/create_cohorts.py "$DEST"
echo 'create hospitals...'
python scripts/create_hospitals.py "$DEST" data/hospitals.csv
echo 'create other groups...'
python scripts/create_other_groups.py "$DEST"
echo 'create source types...'
python scripts/create_source_types.py "$DEST"
echo 'create group diagnoses...'
python scripts/create_group_diagnoses.py "$DEST" data/group_diagnoses.csv
echo 'create observations...'
python scripts/create_observations.py "$DEST" data/observations.csv
echo 'migrate users...'
python scripts/migrate_users.py "$SRC" "$DEST"
echo 'migrate patients...'
python scripts/migrate_patients.py "$SRC" "$DEST"
echo 'migrate pv results...'
python scripts/migrate_pv_results.py "$SRC" "$DEST"
echo 'migrate radar results...'
python scripts/migrate_radar_results.py "$SRC" "$DEST"
echo 'migrate alport...'
python scripts/migrate_alport.py "$SRC" "$DEST"
echo 'migrate consultants...'
python scripts/migrate_consultants.py "$SRC" "$DEST" data/consultants.csv
echo 'migrate dialysis...'
python scripts/migrate_dialysis.py "$SRC" "$DEST"
echo 'migrate diagnosis...'
python scripts/migrate_diagnosis.py "$SRC" "$DEST"
echo 'migrate family histories...'
python scripts/migrate_family_histories.py "$SRC" "$DEST"
echo 'migrate genetics...'
python scripts/migrate_genetics.py "$SRC" "$DEST"
echo 'migrate hnf1b...'
python scripts/migrate_hnf1b.py "$SRC" "$DEST"
echo 'migrate hospitalisations...'
python scripts/migrate_hospitalisations.py "$SRC" "$DEST"
echo 'migrate ins...'
python scripts/migrate_ins.py "$SRC" "$DEST" data/ins_relapse_drugs.csv
echo 'migrate medications...'
python scripts/migrate_medications.py "$SRC" "$DEST"
echo 'migrate mpgn...'
python scripts/migrate_mpgn.py "$SRC" "$DEST"
echo 'migrate pathology...'
python scripts/migrate_pathology.py "$SRC" "$DEST"
echo 'migrate patient addresses...'
python scripts/migrate_patient_addresses.py "$SRC" "$DEST"
echo 'migrate patient aliases...'
python scripts/migrate_patient_aliases.py "$SRC" "$DEST"
echo 'migrate patient numbers...'
python scripts/migrate_patient_numbers.py "$SRC" "$DEST"
echo 'migrate phenotypes...'
python scripts/migrate_phenotypes.py "$SRC" "$DEST"
echo 'migrate plasmapheresis...'
python scripts/migrate_plasmapheresis.py "$SRC" "$DEST"
echo 'migrate transplants...'
python scripts/migrate_transplants.py "$SRC" "$DEST" data/transplant_modalities.csv
echo 'add patients to NEPHROS...'
python scripts/add_patients_to_group.py "$DEST" COHORT NEPHROS data/nephros.csv
echo 'add patients to NSMPGNC3...'
python scripts/add_patients_to_group.py "$DEST" COHORT NSMPGNC3 data/nsmpgnc3.csv
echo 'done'
