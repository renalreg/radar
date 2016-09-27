from radar.models.groups import GROUP_TYPE
from radar.ukrdc_exporter.group_selector import GroupSelector


def export_program_memberships(sda_container, patient):
    program_memberships = sda_container.setdefault('program_memberships', list())

    group_patients = GroupSelector.select_groups(patient.group_patients)

    for group_patient in group_patients:
        group = group_patient.group

        if group.is_radar():
            program_name = 'RADAR'
            program_description = 'RaDaR'
        elif group.type == GROUP_TYPE.COHORT:
            program_name = 'RADAR.{type}.{code}'.format(type=GROUP_TYPE.COHORT, code=group.code)
            program_description = group.name
        else:
            continue

        program_membership = {
            'program_name': program_name,
            'program_description': program_description,
            'from_time': group_patient.from_date
        }

        if group_patient.to_date is not None:
            program_membership['to_time'] = group_patient.to_date

        program_memberships.append(program_membership)
