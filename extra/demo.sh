#!/bin/sh

set -e

cd "$(dirname "$0")"

function cleanup {
  # Remove temporary files
  [[ $tmp ]] && rm -f $tmp

  # Kill SSH background processes
  [[ $pid1 ]] && kill $pid1
  [[ $pid2 ]] && kill $pid2
  wait
}

trap cleanup EXIT

production_db_host=db.radar.nhs.uk
production_db_port=20000
production_db_name=radar
production_db_user=radar
read -s -p "production database password: " production_db_pass
printf '\n'

demo_db_host=demo.radar.nhs.uk
demo_db_port=20001
demo_db_name=radar
demo_db_user=radar
read -s -p "demo database password: " demo_db_pass
printf '\n'

password=password

demo_psql() {
    PGPASSWORD="$demo_db_pass" psql -h localhost -p $demo_db_port -U $demo_db_user $demo_db_name "$@"
}

production_pg_dump() {
    PGPASSWORD="$production_db_pass" pg_dump -h localhost -p $production_db_port -U $production_db_user $production_db_name "$@"
}

fixtures() {
    python fixtures/fixtures.py --connection-string "postgresql://$demo_db_user:$demo_db_pass@localhost:$demo_db_port/$demo_db_name" "$@"
}

echo "starting SSH forwarding..."

# SSH forwarding
ssh -N -L $production_db_port:localhost:5432 $production_db_host &
pid1=$!
ssh -N -L $demo_db_port:localhost:5432 $demo_db_host &
pid2=$!

tmp=$(mktemp)

# HACK give SSH time to connect
sleep 5

echo "dumping database..."

production_pg_dump \
    --data-only \
    --disable-triggers \
    --table consultants \
    --table diagnoses \
    --table drug_groups \
    --table drugs \
    --table group_consultants \
    --table group_diagnoses \
    --table group_observations \
    --table groups \
    --table observations \
    --table posts \
    --table settings \
    --table specialties \
    > "$tmp"

echo "creating schema..."

fixtures drop
fixtures create

echo "importing data..."

cat "$tmp" | demo_psql -v ON_ERROR_STOP=1

echo "creating users..."

fixtures users --password $password

echo "fixing users..."

demo_psql -v ON_ERROR_STOP=1 <<EOF
select id from users where username = 'admin' \gset
update consultants set created_user_id = :id, modified_user_id = :id;
update group_consultants set created_user_id = :id, modified_user_id = :id;
update posts set created_user_id = :id, modified_user_id = :id;
EOF

echo "creating patients..."

fixtures patients --patients 45 --no-data
fixtures patients --patients 5

echo "done"
