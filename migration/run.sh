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

echo 'bootstrap...'
python scripts/bootstrap.py "$DEST"
echo 'create users...'
python scripts/create_users.py "$DEST"
echo 'create cohorts...'
python scripts/create_cohorts.py "$DEST"
echo 'create organisations...'
python scripts/create_organisations.py "$DEST" data/units.csv
echo 'migrate users...'
python scripts/migrate_users.py "$SRC" "$DEST"
echo 'migrate patients...'
python scripts/migrate_patients.py "$SRC" "$DEST"
echo 'migrate alport...'
python scripts/migrate_alport.py "$SRC" "$DEST"
#echo 'migrate consultants...'
#python scripts/migrate_consultants.py "$SRC" "$DEST" data/consultants.csv
echo 'migrate dialysis...'
python scripts/migrate_dialysis.py "$SRC" "$DEST"
echo 'migrate family history...'
python scripts/migrate_family_history.py "$SRC" "$DEST"
echo 'migrate genetics...'
python scripts/migrate_genetics.py "$SRC" "$DEST"
echo 'migrate hnf1b...'
python scripts/migrate_hnf1b.py "$SRC" "$DEST"
echo 'migrate hospitalisations...'
python scripts/migrate_hospitalisations.py "$SRC" "$DEST"
echo 'migrate ins...'
python scripts/migrate_ins.py "$SRC" "$DEST"
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
echo 'migrate plasmapheresis...'
python scripts/migrate_plasmapheresis.py "$SRC" "$DEST"
echo 'migrate transplants...'
python scripts/migrate_transplants.py "$SRC" "$DEST"
echo 'done'
