import argparse
import logging
import os

from radar.database import db

from radar_ukrdc_exporter.tasks import export_to_ukrdc
import fcntl

from radar_ukrdc_exporter.app import create_celery, create_app


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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('--state-file')
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()

    app = create_app()
    celery = create_celery(app)

    if args.state_file:
        if not os.path.exists(args.state_file):
            with open(args.state_file, 'w') as state_f:
                state_f.write(str(0))
                state_f.write('\n')

        state_f = open(args.state_file, 'r+')
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
