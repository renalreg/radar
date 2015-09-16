from radar.lib.data_sources import is_radar_data_source
from radar.lib.models import DATA_SOURCE_TYPE_RADAR


def intersect_patient_and_user_organisations(patient, user, patient_membership=False, user_membership=False):
    organisation_patients = {x.organisation.id: x for x in patient.organisation_patients}

    intersection = []

    for organisation_user in user.organisation_users:
        organisation_id = organisation_user.organisation.id
        organisation_patient = organisation_patients.get(organisation_id)

        if organisation_patient:
            if patient_membership and user_membership:
                intersection.append((organisation_patient, organisation_user))
            elif patient_membership:
                intersection.append(organisation_patient)
            elif user_membership:
                intersection.append(organisation_user)
            else:
                intersection.append(organisation_user.organisation)

    return intersection


def intersect_patient_and_user_cohorts(patient, user, patient_membership=False, user_membership=False):
    cohort_patients = {x.cohort.id: x for x in patient.cohort_patients}

    intersection = []

    for cohort_user in user.cohort_users:
        cohort_id = cohort_user.cohort.id
        cohort_patient = cohort_patients.get(cohort_id)

        if cohort_patient:
            if patient_membership and user_membership:
                intersection.append((cohort_patient, cohort_user))
            elif patient_membership:
                intersection.append(cohort_patient)
            elif user_membership:
                intersection.append(cohort_user)
            else:
                intersection.append(cohort_user.cohort)

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

            # Can only modify RaDaR data (any organisation)
            if data_source.type != DATA_SOURCE_TYPE_RADAR:
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


class RadarObjectPermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(RadarObjectPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        mutate = request.method != 'GET'

        if mutate:
            data_source = obj.data_source

            # Can only modify RaDaR data
            if not is_radar_data_source(data_source):
                return False

        return True


class CohortObjectPermission(Permission):
    def has_object_permission(self, request, user, obj):
        if not super(CohortObjectPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        mutate = request.method != 'GET'

        user_organisations = intersect_patient_and_user_organisations(obj.patient, user, user_membership=True)

        if mutate:
            # Edit permission through organisation membership
            if any(x.has_edit_patient_permission for x in user_organisations):
                return True
        else:
            # View permission through organisation membership
            if any(x.has_view_patient_permission for x in user_organisations):
                return True

            cohort = obj.cohort
            cohort_membership = user.get_disease_group_membership(cohort)

            # View permission through organisation membership
            if cohort_membership is not None and cohort_membership.has_view_patient_permission:
                return True

        return False


class PatientDataSourceObjectPermission(PatientObjectPermission, DataSourceObjectPermission):
    pass


class PatientRadarObjectPermission(PatientObjectPermission, RadarObjectPermission):
    pass
