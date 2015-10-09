from radar.api.serializers.cohort_users import CohortUserSerializer
from radar.lib.models import CohortUser
from radar.lib.roles import COHORT_ROLES
from radar.lib.validation.cohort_users import CohortUserValidation
from radar.lib.views.codes import CodedStringListView
from radar.lib.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView


class CohortUserListView(ListCreateModelView):
    serializer_class = CohortUserSerializer
    model_class = CohortUser
    validation_class = CohortUserValidation


class CohortUserDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = CohortUserSerializer
    model_class = CohortUser
    validation_class = CohortUserValidation


class CohortUserRoleListView(CodedStringListView):
    items = COHORT_ROLES
