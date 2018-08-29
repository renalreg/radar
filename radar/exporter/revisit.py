from datetime import datetime

from sqlalchemy import text

from radar.app import Radar
from radar.database import db
from radar.models import Group


def get_hospitals():
    select_stmt = text('''
        SELECT DISTINCT created_group_id FROM group_patients
        WHERE group_id IN (
            SELECT id FROM groups
            WHERE code = 'NURTUREINS' OR code = 'NURTURECKD'
        )
    ''')
    results = db.session.execute(select_stmt)
    return [row for row, in results]


def revisit():

    nurtureins = Group.query.filter_by(code='NURTUREINS').first()
    nurtureckd = Group.query.filter_by(code='NURTURECKD').first()

    hospital_ids = get_hospitals()
    headers = ['hospital', 'patient_id', 'latest_visit']
    import csv
    import io
    fdesc = io.open('visits.csv', 'w', newline='', encoding='utf-8')
    writer = csv.DictWriter(fdesc, fieldnames=headers)
    writer.writeheader()

    for hospital_id in hospital_ids:
        hospital = Group.query.get(hospital_id)

        # ins_list = PatientList(hospital, nurtureins_primary_diagnoses, 'ins', nurtureins)
        # ckd_list = PatientList(hospital, nurtureckd_primary_diagnoses, 'ckd', nurtureckd)

        for patient in hospital.patients:
            if patient.test or patient.control:
                continue

            if patient.in_group(nurtureckd) or patient.in_group(nurtureins):
                visits = {}
                for entry in patient.entries:
                    if entry.form.slug != 'nurtureckd':
                        continue

                    visit = datetime.strptime(entry.data['date'], '%Y-%m-%d').date()
                    visits[visit] = entry.data
                    headers

                if not visits:
                    continue

                latest = sorted(visits)[-1]

                if latest < datetime(2017, 10, 1).date():
                    writer.writerow({
                        'hospital': hospital.name,
                        'patient_id': patient.id,
                        'latest_visit': latest.strftime('%Y-%m-%d')
                    })

    fdesc.close()
    #     ckd_list.append(p)
    # elif p.in_group(nurtureins):
    #     ins_list.append(p)
    # ckd_list.export()
    # ins_list.export()
    # print(hospital_id)


def main():
    app = Radar()

    with app.app_context():
        revisit()


if __name__ == '__main__':
    main()
