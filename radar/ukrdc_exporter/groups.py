from radar.models.groups import GROUP_TYPE
from radar.ukrdc_exporter.group_selector import GroupSelector


def export_program_memberships(sda_container, patient, system_group):
    program_memberships = sda_container.setdefault('program_memberships', list())

    group_patients = GroupSelector.select_groups(patient.group_patients)

    # Export memberships for this system and its cohorts
    for group_patient in group_patients:
        group = group_patient.group

        if group == system_group:
            program_name = group.code
            program_description = group.name
        elif group.parent_group == system_group and group.type == GROUP_TYPE.COHORT:
            program_name = '{0}.{1}.{2}'.format(system_group.code, group.type, group.code)
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
