from radar.api.views.common import StringLookupListView
from radar.roles import ROLE_NAMES


class RoleListView(StringLookupListView):
    items = ROLE_NAMES


def register_views(app):
    app.add_url_rule('/roles', view_func=RoleListView.as_view('role_list'))
