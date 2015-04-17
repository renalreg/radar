from flask import render_template, request, abort, url_for, redirect
from flask.views import View
from flask_login import current_user
from radar.services import get_unit_filters_for_user, get_disease_group_filters_for_user, get_users_for_user, \
    get_user_for_user
from radar.users.forms import UserSearchFormHandler, UserDiseaseGroupFormHandler, UserUnitFormHandler
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

class UserDetailView(BaseView):
    def dispatch_request(self, user_id):
        user = get_user_for_user(current_user, user_id)

        if user is None:
            abort(404)

        context = self.get_context()

        context['user'] = user

        # TODO
        context['disease_group_form'] = UserDiseaseGroupFormHandler()
        context['unit_form'] = UserUnitFormHandler()
        context['disease_group_choices'] = [(x.name, x.id) for x in get_disease_group_filters_for_user(current_user)]
        context['unit_choices'] = [(x.name, x.id) for x in get_unit_filters_for_user(current_user)]

        return render_template('user.html', **context)

class UserDiseaseGroupsView(View):
    methods = ['POST']

    # TODO
    def dispatch_request(self, user_id):
        return redirect(url_for('user', user_id=user_id))

class UserUnitsView(View):
    methods = ['POST']

    # TODO
    def dispatch_request(self, user_id):
        return redirect(url_for('user', user_id=user_id))