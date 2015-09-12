from operator import or_

from flask import request

from radar.lib.database import db
from radar.lib.models import CohortPatient, Cohort, CohortUser, OrganisationPatient, Organisation
from radar.lib.permissions import CohortObjectPermission
from radar.lib.roles import COHORT_VIEW_PATIENT_ROLES, ORGANISATION_VIEW_PATIENT_ROLES
from radar.lib.serializers import Serializer, IntegerField
from radar.lib.auth import current_user


class CohortRequestSerializer(Serializer):
    cohort = IntegerField()


class CohortObjectViewMixin(object):
    def get_permission_classes(self):
        permission_classes = super(CohortObjectViewMixin, self).get_permission_classes()
        permission_classes.append(CohortObjectPermission)
        return permission_classes

    def filter_query(self, query):
        query = super(CohortObjectViewMixin, self).filter_query(query)

        # Filter the query based on the user's organisation and cohort membership
        # Admins can view all data so don't filter their queries
        if not current_user.is_admin:
            model_class = self.get_model_class()

            # Check if the user has permission through their cohort membership (requires the view patient permission).
            cohort_sub_query = db.session.query(CohortPatient)\
                .join(CohortPatient.cohort)\
                .join(Cohort.cohort_users)\
                .filter(
                    CohortPatient.patient_id == model_class.patient_id,
                    CohortPatient.cohort_id == model_class.cohort_id,
                    CohortUser.user == current_user,
                    CohortUser.role.in_(COHORT_VIEW_PATIENT_ROLES)
                )\
                .exists()

            # Check if the user has permission through their organisation membership. If the user has the view patient
            # permission on one of the patient's units they can view all disease group data.
            organisation_sub_query = db.session.query(OrganisationPatient)\
                .join(OrganisationPatient.organisation)\
                .join(Organisation.organisation_users)\
                .filter(
                    OrganisationPatient.patient_id == model_class.patient_id,
                    Organisation.user == current_user,
                    Organisation.role.in_(ORGANISATION_VIEW_PATIENT_ROLES)
                )\
                .exists()

            # Filter the query to only include rows the user has permission to see
            # Permission is granted through the user's disease group membership and/or unit membership
            query = query.filter(or_(
                cohort_sub_query,
                organisation_sub_query
            ))

        serializer = CohortRequestSerializer()
        args = serializer.to_value(request.args)

        # Filter by cohort
        # Note: we don't check permissions here as the query has already been filtered. If the user doesn't belong to
        # the cohort no results will be returned.
        if 'cohort' in args:
            model_class = self.get_model_class()
            query = query.filter(model_class.cohort_id == args['cohort'])

        return query
