#!/usr/bin/env python

import argparse
import logging
import os
import fcntl

from radar.database import db
from radar.ukrdc_exporter.app import RadarUKRDCExporter
from radar.ukrdc_exporter.tasks import export_to_ukrdc


logger = logging.getLogger()


sql = """
select id, patient_id from (
    select distinct
        id, (data->'new_data'->>'patient_id')::integer as patient_id
    from logs
    where
        (type = 'INSERT' or type = 'UPDATE') and
        (data->'new_data'->>'patient_id')::integer is not null and
        ((data->'new_data'->>'source_type')::text is null or (data->'new_data'->>'source_type')::text = 'RADAR') and
        id > :last_log_id

    union

    select
        id, (data->'original_data'->>'patient_id')::integer
    from logs
    where
        (type = 'UPDATE' or type = 'DELETE') and
        (data->'original_data'->>'patient_id')::integer is not null and
        ((data->'original_data'->>'source_type')::text is null or (data->'original_data'->>'source_type')::text = 'RADAR') and
        id > :last_log_id
) as x order by id
"""


def export_patients(last_log_id=0):
    rows = db.session.execute(sql, {'last_log_id': last_log_id})
    patient_ids = set()

    for log_id, patient_id in rows:
        last_log_id = log_id

        if patient_id in patient_ids:
            continue

        logger.info('Adding patient to queue id={}'.format(patient_id))
        export_to_ukrdc(patient_id)
        patient_ids.add(patient_id)

    return last_log_id


def lock(f):
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()

    app = RadarUKRDCExporter()

    state = app.config['EXPORT_STATE']

    if state is not None:
        if not os.path.exists(state):
            with open(state, 'w') as state_f:
                state_f.write(str(0))
                state_f.write('\n')

        state_f = open(state, 'r+')
        lock(state_f)

        if args.all:
            last_log_id = 0
        else:
            last_log_id = int(state_f.readline())
    else:
        state_f = None
        last_log_id = 0

    with app.app_context():
        last_log_id = export_patients(last_log_id)

    if state_f is not None:
        state_f.seek(0)
        state_f.write(str(last_log_id))
        state_f.write('\n')
        state_f.truncate()
        state_f.close()


if __name__ == '__main__':
    main()
