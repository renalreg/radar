from radar_api.serializers.user_sessions import UserSessionSerializer
from radar.auth.sessions import current_user
from radar.models.user_sessions import UserSession
from radar.views.core import ListModelView


class UserSessionListView(ListModelView):
    serializer_class = UserSessionSerializer
    model_class = UserSession

    def filter_query(self, query):
        # Only show active sessions for the current user
        query = query\
            .filter(UserSession.user == current_user)\
            .filter(UserSession.is_active)

        return query
