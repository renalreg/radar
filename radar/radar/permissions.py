from radar.data_sources import is_radar_data_source
from radar.models import DATA_SOURCE_TYPE_RADAR


def has_group_permission_for_patient(user, patient, permission):
    if user.is_admin:
        grant = True
    else:
        grant = has_organisation_permission_for_patient(user, patient, permission)

        if not grant:
            grant = has_cohort_permission_for_patient(user, patient, permission)

    return grant


def has_organisation_permission_for_patient(user, patient, permission):
    if user.is_admin:
        return True
    else:
        organisation_users = intersect_patient_and_user_organisations(patient, user, user_membership=True)
        return any(getattr(x, permission) for x in organisation_users)


def has_cohort_permission_for_patient(user, patient, permission):
    if user.is_admin:
        return True
    else:
        cohort_users = intersect_patient_and_user_cohorts(patient, user, user_membership=True)
        return any(getattr(x, permission) for x in cohort_users)


def has_cohort_permission(user, cohort, permission):
    if user.is_admin:
        return True
    else:
        for cohort_user in user.cohort_users:
            # User is a member of the cohort and has the view patient permission
            if cohort_user.cohort == cohort and cohort_user.has_view_patient_permission:
                return True

        return False


def has_organisation_permission(user, organisation, permission):
    if user.is_admin:
        return True
    else:
        for organisation_user in user.organisation_users:
            # User is a member of the organisation and has the edit patient permission
            if organisation_user.organisation == organisation and organisation_user.has_edit_patient_permission:
                return True

        return False


def can_view_demographics(user, patient):
    return has_group_permission_for_patient(user, patient, 'has_view_demographics_permission')


def can_view_patient(user, patient, cohort=None):
    if user.is_admin:
        return True

    if not has_group_permission_for_patient(user, patient, 'has_view_patient_permission'):
        return False

    if cohort is not None and not has_cohort_permission(user, cohort, 'has_view_patient_permission'):
        return False

    return True


def can_edit_patient(user, patient, organisation=None):
    if user.is_admin:
        return True

    if not has_organisation_permission_for_patient(user, patient, 'has_edit_patient_permission'):
        return False

    if organisation is not None and not has_organisation_permission(user, organisation, 'has_edit_patient_permission'):
        return False

    return True


def intersect_patient_and_user_organisations(patient, user, patient_membership=False, user_membership=False):
    organisation_patients = {x.organisation: x for x in patient.organisation_patients}

    intersection = []

    for organisation_user in user.organisation_users:
        organisation = organisation_user.organisation
        organisation_patient = organisation_patients.get(organisation)

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
    cohort_patients = {x.cohort: x for x in patient.cohort_patients}

    intersection = []

    for cohort_user in user.cohort_users:
        cohort = cohort_user.cohort
        cohort_patient = cohort_patients.get(cohort)

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


def is_write_request(request):
    return request.method not in ['GET', 'HEAD']


class Permission(object):
    def has_permission(self, request, user):
        return True

    def has_object_permission(self, request, user, obj):
        return True


class PatientPermission(Permission):
    """Checks that the user can view or update a patient.

    Permission is granted if:
    * The user is an admin.
    * The user is updating the patient and they have the edit patient permission
      through their group membership.
    * The user is viewing the patient and they have the view patient permission
      through their group membership.
    """

    def has_object_permission(self, request, user, obj):
        if not super(PatientPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        if is_write_request(request):
            return can_edit_patient(user, obj)
        else:
            return can_view_patient(user, obj)


class PatientObjectPermission(PatientPermission):
    """Checks that the user has permission to view or update a patient object.

    Permission is granted if:
    * The user is an admin.
    * The user is updating the object and has the edit patient permission
      through their organisation membership.
    * The user is viewing the object and has the view patient permission through
      their group membership (organisations and cohorts).
    """

    def has_object_permission(self, request, user, obj):
        return super(PatientObjectPermission, self).has_object_permission(request, user, obj.patient)


class DataSourceObjectPermission(Permission):
    """Checks that the user has permission to edit an object belonging to a data source.

    Permission is granted if:
    * The user is an admin.
    * The user is updating the object and the object was entered on RaDaR and
      the user has permission to edit objects belonging to this data source
      (through their organisation membership).
    * The user is only viewing the object. Permissions for this are handled in
      PatientObjectPermission.
    """

    def has_object_permission(self, request, user, obj):
        if not super(DataSourceObjectPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        if is_write_request(request):
            data_source = obj.data_source

            # Can only modify RaDaR data (any organisation)
            if data_source.type != DATA_SOURCE_TYPE_RADAR:
                return False

            organisation = data_source.organisation
            patient = obj.patient

            return can_edit_patient(user, patient, organisation=organisation)
        else:
            # Users can view data from data sources they aren't members of
            return True


class RadarObjectPermission(Permission):
    """Ensures that only objects from the RaDaR data source can be edited.

    Permission is granted:
    * The user is an admin.
    * The user is updating the object and the object belongs to the RaDaR
      data source.
    * The user is only viewing the object. This permission doesn't restrict
      which data sources a user can view.
    """

    def has_object_permission(self, request, user, obj):
        if not super(RadarObjectPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        if is_write_request(request):
            data_source = obj.data_source

            # Can only modify RaDaR data
            return is_radar_data_source(data_source)
        else:
            # This permission only affects which objects can be edited
            return True


class CohortObjectPermission(Permission):
    """Checks that the user has permission to view an object belonging to a cohort.

    Permission is granted if:
    * The user is an admin.
    * The user is attempting to update the object. The CohortObjectPermission
      should be used in conjunction with the PatientObjectPermission. The
      PatientObjectPermission checks that the user has permission to edit the
      patient.
    * The object is being viewed and the user has permission to view this
      patient (through their organisation or cohort membership) and they also
      have permission to view the object's cohort. If the user can view the
      patient through their organisation membership they can view data belonging
      to any cohort. Otherwise the patient and user need to be in the same
      cohort and the user needs to also have the view patient permission for
      that cohort.
    """

    def has_object_permission(self, request, user, obj):
        if not super(CohortObjectPermission, self).has_object_permission(request, user, obj):
            return False

        if user.is_admin:
            return True

        # Updating the object
        if is_write_request(request):
            # The CohortObjectPermission class should be used with the
            # PatientObjectPermission class. The PatientObjectPermission class
            # will check the user has permission to edit this patient's data.
            return True
        else:
            patient = obj.patient

            # User isn't allowed to view this patient
            if not can_view_patient(user, patient):
                return False

            cohort = obj.cohort

            # Check the user has the view patient permission for the object's
            # cohort. This prevents users viewing data from other cohorts even
            # if they have permission to view the patient.
            return can_view_patient(user, patient, cohort=cohort)


class PatientDataSourceObjectPermission(PatientObjectPermission, DataSourceObjectPermission):
    pass


class PatientRadarObjectPermission(PatientObjectPermission, RadarObjectPermission):
    pass


class PatientCohortObjectPermission(PatientObjectPermission, CohortObjectPermission):
    pass
