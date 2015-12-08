from radar_api.serializers.cohort_users import CohortUserSerializer
from radar.models import CohortUser
from radar.roles import COHORT_ROLE_NAMES
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
    items = COHORT_ROLE_NAMES


def register_views(app):
    app.add_url_rule('/cohort-users', view_func=CohortUserListView.as_view('cohort_user_list'))
    app.add_url_rule('/cohort-users/<int:id>', view_func=CohortUserDetailView.as_view('cohort_user_detail'))
    app.add_url_rule('/cohort-user-roles', view_func=CohortUserRoleListView.as_view('cohort_user_role_list'))
