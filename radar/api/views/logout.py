from flask import Response

from radar.api.views.generics import ApiView
from radar.auth.sessions import logout, logout_other_sessions


class LogoutView(ApiView):
    def post(self):
        logout()
        return Response(status=200)


class LogoutOtherSessionsView(ApiView):
    def post(self):
        logout_other_sessions()
        return Response(status=200)


def register_views(app):
    app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
    app.add_url_rule('/logout-other-sessions', view_func=LogoutOtherSessionsView.as_view('logout_other_sessions'))
