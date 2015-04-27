from flask import render_template, request, abort, url_for, redirect
from flask.views import View
from flask_login import current_user
from radar.services import get_unit_filters_for_user, get_disease_group_filters_for_user, get_users_for_user, \
    get_user_for_user, filter_user_disease_groups_for_user, filter_user_units_for_user
from radar.views import get_base_context


def get_user_base_context():
    context = get_base_context()

    context.update({
        'filter_user_units_for_user': filter_user_units_for_user,
        'filter_user_disease_groups_for_user': filter_user_disease_groups_for_user,
    })

    return context

def get_user_detail_context(user_id):
    context = get_user_base_context()

    user = get_user_for_user(current_user, user_id)

    if user is None:
        abort(404)

    context['user'] = user

    return context

class UserListView(View):
    def dispatch_request(self):
        search = {}
        form = UserSearchFormHandler(search)
        form.submit(request.args)

        users = get_users_for_user(current_user, search)

        unit_choices = [(x.name, x.id) for x in get_unit_filters_for_user(current_user)]
        disease_group_choices = [(x.name, x.id) for x in get_disease_group_filters_for_user(current_user)]

        context = get_user_base_context()
        context['users'] = users
        context['form'] = form
        context['disease_group_choices'] = disease_group_choices
        context['unit_choices'] = unit_choices

        return render_template('users.html', **context)

class UserDetailView(View):
    def dispatch_request(self, user_id):
        context = get_user_detail_context(user_id)

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