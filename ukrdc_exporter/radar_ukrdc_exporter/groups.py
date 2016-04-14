def export_program_memberships(sda_container, patient):
    program_memberships = sda_container.setdefault('program_memberships', list())

    # TODO
    program_membership = {
        'from_time': patient.recruited_date,
        'program_name': 'RaDaR',
        'program_description': 'RaDaR'
    }

    program_memberships.append(program_membership)
