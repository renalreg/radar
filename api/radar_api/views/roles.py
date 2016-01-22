from radar.views.codes import CodedStringListView
from radar.roles import ROLE_NAMES


class RoleListView(CodedStringListView):
    items = ROLE_NAMES


def register_views(app):
    app.add_url_rule('/roles', view_func=RoleListView.as_view('role_list'))
