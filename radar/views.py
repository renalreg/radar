from flask import render_template, abort
from flask.views import View
from flask_login import current_user

from radar.services import get_disease_groups_for_user, get_units_for_user, get_unit_for_user, \
    get_disease_group_for_user, can_user_list_patients


def get_base_context():
    context = dict()

    if current_user.is_authenticated():
        context['user_units'] = get_units_for_user(current_user)
        context['user_disease_groups'] = get_disease_groups_for_user(current_user)
        context['can_view_patients'] = can_user_list_patients(current_user)

    return context


class IndexView(View):
    def dispatch_request(self):
        context = get_base_context()
        return render_template('index.html', **context)


class DiseaseGroupsView(View):
    def dispatch_request(self):
        context = get_base_context()
        return render_template('disease_groups.html', **context)


class DiseaseGroupView(View):
    def dispatch_request(self, disease_group_id):
        disease_group = get_disease_group_for_user(current_user, disease_group_id)

        if disease_group is None:
            abort(404)

        context = get_base_context()
        context['disease_group'] = disease_group

        return render_template('disease_group.html', **context)


class UnitsView(View):
    def dispatch_request(self):
        context = get_base_context()
        return render_template('units.html', **context)


class UnitView(View):
    def dispatch_request(self, unit_id):
        unit = get_unit_for_user(current_user, unit_id)

        if unit is None:
            abort(404)

        context = get_base_context()
        context['unit'] = unit

        return render_template('unit.html', **context)


class AdminView(View):
    def dispatch_request(self):
        context = get_base_context()
        return render_template('admin.html', **context)