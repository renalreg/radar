from radar.models.groups import GROUP_TYPE
from radar.ukrdc_exporter.group_selector import GroupSelector


def export_program_memberships(rda_container, patient, groups):
    program_memberships = rda_container.setdefault('program_memberships', [])

    group_patients = GroupSelector.select_groups(patient.group_patients)

    # Export memberships for this system and its cohorts
    systems = [group for group in groups if group.type == GROUP_TYPE.SYSTEM]
    for group_patient in group_patients:
        group = group_patient.group

        if group in systems:
            program_name = group.code
            program_description = group.name
        elif group.parent_group in systems and group.type == GROUP_TYPE.COHORT:
            program_name = '{0}.{1}.{2}'.format(group.parent_group.code, group.type, group.code)
            program_description = group.name
        else:
            continue

        program_membership = {
            'external_id': group_patient.id,
            'program_name': program_name,
            'program_description': program_description,
            'from_time': group_patient.from_date
        }

        if group_patient.to_date is not None:
            program_membership['to_time'] = group_patient.to_date

        program_memberships.append(program_membership)
