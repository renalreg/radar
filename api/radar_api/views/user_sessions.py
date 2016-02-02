from radar_api.serializers.user_sessions import UserSessionSerializer
from radar.auth.sessions import current_user
from radar.models.user_sessions import UserSession
from radar.views.core import ListModelView


class UserSessionListView(ListModelView):
    serializer_class = UserSessionSerializer
    model_class = UserSession

    def filter_query(self, query):
        query = super(UserSessionListView, self).filter_query(query)

        # Only show active sessions for the current user
        query = query.filter(UserSession.user == current_user)

        return query


def register_views(app):
    app.add_url_rule('/user-sessions', view_func=UserSessionListView.as_view('user_session_list'))
