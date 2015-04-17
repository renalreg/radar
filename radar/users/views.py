from flask import render_template, request
from flask_login import current_user
from radar.services import get_unit_filters_for_user, get_disease_group_filters_for_user, get_users_for_user
from radar.users.forms import UserSearchFormHandler
from radar.views import BaseView


class UserListView(BaseView):
    def dispatch_request(self):
        search = {}
        form = UserSearchFormHandler(search)
        form.submit(request.args)

        users = get_users_for_user(current_user, search)

        unit_choices = [(x.name, x.id) for x in get_unit_filters_for_user(current_user)]
        disease_group_choices = [(x.name, x.id) for x in get_disease_group_filters_for_user(current_user)]

        context = self.get_context()
        context['users'] = users
        context['form'] = form
        context['disease_group_choices'] = disease_group_choices
        context['unit_choices'] = unit_choices

        return render_template('users.html', **context)