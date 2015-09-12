from radar.lib.models import DATA_SOURCE_TYPE_RADAR


def intersect_patient_and_user_organisations(patient, user, patient_membership=False, user_membership=False):
    unit_patients = {x.organisation.id: x for x in patient.unit_patients}

    intersection = []

    for unit_user in user.unit_users:
        unit_id = unit_user.organisation.id
        unit_patient = unit_patients.get(unit_id)

        if unit_patient:
            if patient_membership and user_membership:
                intersection.append((unit_patient, unit_user))
            elif patient_membership:
                intersection.append(unit_patient)
            elif user_membership:
                intersection.append(unit_user)
            else:
                intersection.append(unit_user.organisation)

    return intersection


def intersect_patient_and_user_cohorts(patient, user, patient_membership=False, user_membership=False):
    disease_group_patients = {x.cohort.id: x for x in patient.cohort_patients}

    intersection = []

    for disease_group_user in user.disease_group_users:
        disease_group_id = disease_group_user.cohort.id
        disease_group_patient = disease_group_patients.get(disease_group_id)

        if disease_group_patient:
            if patient_membership and user_membership:
                intersection.append((disease_group_patient, disease_group_user))
            elif patient_membership:
                intersection.append(disease_group_patient)
            elif user_membership:
                intersection.append(disease_group_user)
            else:
                intersection.append(disease_group_user.cohort)

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

        user_units = intersect_patient_and_user_organisations(obj, user, user_membership=True)

        if mutate:
            # Edit permission through unit membership
            if any(x.has_edit_patient_permission for x in user_units):
                return True
        else:
            # View permission through unit membership
            if any(x.has_view_patient_permission for x in user_units):
                return True

            user_disease_groups = intersect_patient_and_user_cohorts(obj, user, user_membership=True)

            # View permission through disease group membership
            if any(x.has_view_patient_permission for x in user_disease_groups):
                return True

        return False


class PatientObjectPermission(PatientPermission):
    def has_object_permission(self, request, user, obj):
        return super(PatientObjectPermission, self).has_object_permission(request, user, obj.patient)


class DataSourceObjectPermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(DataSourceObjectPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        mutate = request.method != 'GET'

        if mutate:
            data_source = obj.data_source

            # Can only modify RaDaR data
            if not data_source.type != DATA_SOURCE_TYPE_RADAR:
                return False

            organisation = data_source.organisation

            grant = False

            for organisation_user in user.organisation_users:
                # User is a member of the organisation and has the edit patient permission
                if organisation_user.organisation == organisation and organisation_user.has_edit_patient_permission:
                    grant = True

            if not grant:
                return False

        return True


class CohortObjectPermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(CohortObjectPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        mutate = request.method != 'GET'

        user_units = intersect_patient_and_user_organisations(obj.patient, user, user_membership=True)

        if mutate:
            # Edit permission through organisation membership
            if any(x.has_edit_patient_permission for x in user_units):
                return True
        else:
            # View permission through organisation membership
            if any(x.has_view_patient_permission for x in user_units):
                return True

            disease_group = obj.cohort
            disease_group_membership = user.get_disease_group_membership(disease_group)

            # View permission through organisation membership
            if disease_group_membership is not None and disease_group_membership.has_view_patient_permission:
                return True

        return False


class PatientDataSourceObjectPermission(PatientObjectPermission, DataSourceObjectPermission):
    pass
