#!/usr/bin/env python

import argparse
import logging
import os
import fcntl

from radar.database import db
from radar.ukrdc_exporter.app import RadarUKRDCExporter
from radar.ukrdc_exporter.tasks import export_to_ukrdc


logger = logging.getLogger()


changed_sql = """
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

all_sql = """
select x.id, patients.id from patients
left join ({0}) as x on patients.id = x.patient_id
order by x.id, patients.id
""".format(changed_sql)


def export_all(last_log_id):
    return export_query(all_sql, last_log_id)


def export_changed(last_log_id):
    return export_query(changed_sql, last_log_id)


def export_query(sql, last_log_id):
    rows = db.session.execute(sql, {'last_log_id': last_log_id})

    patient_ids = []

    for log_id, patient_id in rows:
        if log_id is not None:
            last_log_id = log_id

        patient_ids.append(patient_id)

    export_patients(patient_ids)

    return last_log_id


def export_patients(patient_ids):
    for patient_id in sorted(set(patient_ids)):
        logger.info('Adding patient to queue id={}'.format(patient_id))
        export_to_ukrdc(patient_id)


def lock(f):
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--all', action='store_true')
    group.add_argument('--changed', action='store_true')
    group.add_argument('--id', type=int, dest='patient_ids', action='append', default=[])
    args = parser.parse_args()

    app = RadarUKRDCExporter()

    if args.all or args.changed:
        state = app.config['UKRDC_EXPORTER_STATE']

        if state is not None:
            if not os.path.exists(state):
                with open(state, 'w') as state_f:
                    state_f.write(str(0))
                    state_f.write('\n')

            state_f = open(state, 'r+')
            lock(state_f)
            last_log_id = int(state_f.readline())
        else:
            state_f = None
            last_log_id = 0

        with app.app_context():
            if args.all:
                last_log_id = export_all(last_log_id)
            else:
                last_log_id = export_changed(last_log_id)

        if state_f is not None:
            state_f.seek(0)
            state_f.write(str(last_log_id))
            state_f.write('\n')
            state_f.truncate()
            state_f.close()
    elif args.patient_ids:
        export_patients(args.patient_ids)


if __name__ == '__main__':
    main()
