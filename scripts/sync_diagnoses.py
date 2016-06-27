from __future__ import print_function

import csv
import logging

from radar.app import Radar
from radar.database import db
from radar.models.diagnoses import Diagnosis, GROUP_DIAGNOSIS_TYPE, GroupDiagnosis
from radar.models.groups import Group, GROUP_TYPE


logger = logging.getLogger(__name__)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(logging.INFO)


def parse_groups(value, type):
    if value:
        codes = [x.strip() for x in value.split(',')]
        groups = []

        for code in codes:
            group = Group.query.filter(Group.type == GROUP_TYPE.COHORT, Group.code == code).first()

            if group is None:
                raise ValueError('Group not found "{0}"'.format(code))

            groups.append(group)

        groups = [(x, type) for x in groups]
    else:
        groups = []

    return groups


def sync_groups(diagnosis, new_groups):
    for old_group in diagnosis.group_diagnoses:
        found = False

        for new_group in new_groups:
            if old_group.group == new_group[0] and old_group.type == new_group[1]:
                found = True
                break

        if not found:
            logger.info('Removed "{0}" from "{1}" ({2})'.format(diagnosis.name, old_group.group.code, old_group.type))
            db.session.delete(old_group)

    for new_group in new_groups:
        found = False

        for old_group in diagnosis.group_diagnoses:
            if new_group[0] == old_group.group and new_group[1] == old_group.type:
                found = True
                break

        if not found:
            logger.info('Added "{0}" to "{1}" ({2})'.format(diagnosis.name, new_group[0].code, new_group[1]))
            group_diagnosis = GroupDiagnosis()
            group_diagnosis.diagnosis = diagnosis
            group_diagnosis.group = new_group[0]
            group_diagnosis.type = new_group[1]
            db.session.add(group_diagnosis)


def main(args):
    reader = csv.reader(open(args.src))
    writer = csv.writer(open(args.dest, 'w'))

    # Skip headers
    next(reader)

    for row in reader:
        row = [x.strip() for x in row]

        if row[0]:
            diagnosis_id = int(row[0])
        else:
            diagnosis_id = None

        name = row[1]

        groups = []
        groups += parse_groups(row[2], GROUP_DIAGNOSIS_TYPE.PRIMARY)
        groups += parse_groups(row[3], GROUP_DIAGNOSIS_TYPE.SECONDARY)

        if diagnosis_id is None:
            diagnosis = Diagnosis()

            logger.info('Created "{0}"'.format(name))
        else:
            diagnosis = Diagnosis.query.get(diagnosis_id)

            if diagnosis is None:
                raise ValueError('Diagnosis not found "{0}"'.format(diagnosis_id))

            if diagnosis.name != name:
                logger.info('Renamed "{0}" to "{1}"'.format(diagnosis.name, name))

        diagnosis.name = name
        db.session.add(diagnosis)

        sync_groups(diagnosis, groups)

        db.session.flush()

        row[0] = diagnosis.id
        writer.writerow(row)

    if not args.dry_run:
        db.session.commit()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('src')
    parser.add_argument('dest')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--connection-string', default='postgresql://radar:password@localhost/radar')
    args = parser.parse_args()

    app = Radar({
        'SQLALCHEMY_DATABASE_URI': args.connection_string,
    })

    with app.app_context():
        main(args)
