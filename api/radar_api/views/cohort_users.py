from radar_api.serializers.cohort_users import CohortUserSerializer
from radar.models import CohortUser
from radar.roles import COHORT_ROLES
from radar.validation.cohort_users import CohortUserValidation
from radar.views.codes import CodedStringListView
from radar.views.core import ListCreateModelView, RetrieveUpdateDestroyModelView


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
