#!/bin/sh

set -e

SRC=$1
DEST=$2

echo 'bootstrap...'
python scripts/bootstrap.py "$DEST"
echo 'create users...'
python scripts/create_users.py "$DEST"
echo 'create cohorts...'
python scripts/create_cohorts.py "$DEST"
echo 'create organisations...'
python scripts/create_organisations.py data/units.csv "$DEST"
echo 'migrate users...'
python scripts/migrate_users.py "$SRC" "$DEST"
echo 'migrate patients...'
python scripts/migrate_patients.py "$SRC" "$DEST"
echo 'migrate hospitalisations...'
python scripts/migrate_hospitalisations.py "$SRC" "$DEST"
echo 'done'
