def has_disease_group_role(user, roles):
    if user.is_admin:
        return True

    for disease_group_user in user.disease_groups:
        if disease_group_user.role in roles:
            return True

    return False

def has_unit_role(user, roles):
    if user.is_admin:
        return True

    for unit_user in user.units:
        if unit_user.role in roles:
            return True

    return False

def has_disease_group_role_for_patient(user, patient, roles):
    if user.is_admin:
        return True

    patient_dg_ids = set([x.disease_group_id for x in patient.disease_groups])

    for dg_user in user.disease_groups:
        # * User and patient are in the unit
        # * User has one of the specified roles at the unit
        if dg_user.disease_group_id in patient_dg_ids and dg_user.role in roles:
            return True

    return False

def has_unit_role_for_patient(user, patient, roles):
    if user.is_admin:
        return True

    patient_unit_ids = set([x.unit_id for x in patient.units])

    for unit_user in user.units:
        # * User and patient are in the unit
        # * User has one of the specified roles at the unit
        if unit_user.unit_id in patient_unit_ids and unit_user.role in roles:
            return True

    return False
