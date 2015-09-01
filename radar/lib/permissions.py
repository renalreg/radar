from flask import abort


def intersect_units(patient, user, patient_membership=False, user_membership=False):
    unit_patients = {x.unit.id: x for x in patient.unit_patients}

    intersection = []

    for unit_user in user.unit_users:
        unit_id = unit_user.unit.id
        unit_patient = unit_patients.get(unit_id)

        if unit_patient:
            if patient_membership and user_membership:
                intersection.append((unit_patient, unit_user))
            elif patient_membership:
                intersection.append(unit_patient)
            elif user_membership:
                intersection.append(unit_user)
            else:
                intersection.append(unit_user.unit)

    return intersection


def intersect_disease_groups(patient, user, patient_membership=False, user_membership=False):
    disease_group_patients = {x.disease_group.id: x for x in patient.disease_group_patients}

    intersection = []

    for disease_group_user in user.disease_group_users:
        disease_group_id = disease_group_user.disease_group.id
        disease_group_patient = disease_group_patients.get(disease_group_id)

        if disease_group_patient:
            if patient_membership and user_membership:
                intersection.append((disease_group_patient, disease_group_user))
            elif patient_membership:
                intersection.append(disease_group_patient)
            elif user_membership:
                intersection.append(disease_group_user)
            else:
                intersection.append(disease_group_user.disease_group)

    return intersection


class Permission(object):
    def has_permission(self, request, user):
        return True

    def has_object_permission(self, request, user, obj):
        return True


class PatientPermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(PatientPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        mutate = request.method != 'GET'

        user_units = intersect_units(obj, user, user_membership=True)

        if mutate:
            # Edit permission through unit membership
            if any(x.has_edit_patient_permission for x in user_units):
                return True
        else:
            # View permission through unit membership
            if any(x.has_view_patient_permission for x in user_units):
                return True

            user_disease_groups = intersect_disease_groups(obj, user, user_membership=True)

            # View permission through disease group membership
            if any(x.has_view_patient_permission for x in user_disease_groups):
                return True

        return False


class PatientDataPermission(PatientPermission):
    def has_object_permission(self, request, user, obj):
        return super(PatientDataPermission, self).has_object_permission(request, user, obj.patient)


class FacilityDataPermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(FacilityDataPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        mutate = request.method != 'GET'

        if mutate:
            facility = obj.facility

            # Can't modify external data
            if not facility.is_internal:
                return False

            unit = facility.unit

            # Data doesn't belong to a unit
            if unit is None:
                return True

            unit_membership = user.get_unit_membership(unit)

            # User is not a member of the unit
            if unit_membership is None:
                return False

            # User is a member of the unit but has no edit permission
            if not unit_membership.has_edit_patient_permission:
                return False

        return True


class DiseaseGroupDataPermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(DiseaseGroupDataPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        mutate = request.method != 'GET'

        user_units = intersect_units(obj.patient, user, user_membership=True)

        if mutate:
            # Edit permission through unit membership
            if any(x.has_edit_patient_permission for x in user_units):
                return True
        else:
            # View permission through unit membership
            if any(x.has_view_patient_permission for x in user_units):
                return True

            disease_group = obj.disease_group
            disease_group_membership = user.get_disease_group_membership(disease_group)

            # View permission through unit membership
            if disease_group_membership is not None and disease_group_membership.has_view_patient_permission:
                return True

        return False


class PatientFacilityDataPermission(PatientDataPermission, FacilityDataPermission):
    pass


class IsAuthenticated(Permission):
    def has_permission(self, request, user):
        if not user.is_authenticated():
            abort(401)

        return True
