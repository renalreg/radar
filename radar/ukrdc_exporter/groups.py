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
        else:
            continue

        program_membership = {
            'external_id': str(group_patient.id),
            'program_name': program_name,
            'program_description': program_description,
            'from_time': group_patient.from_date.date()
        }

        if group_patient.to_date is not None:
            program_membership['to_time'] = group_patient.to_date.date()

        program_memberships.append(program_membership)
