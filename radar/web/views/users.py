from flask import render_template, request, abort, Blueprint, flash, url_for, redirect
from flask_login import current_user

from radar.lib.auth import generate_password
from radar.lib.database import db
from radar.lib.disease_groups import get_disease_groups_for_user_with_permissions
from radar.models.disease_groups import DiseaseGroup, DiseaseGroupUser
from radar.lib.ordering import order_query
from radar.lib.pagination import paginate_query
from radar.lib.units import get_units_for_user_with_permissions
from radar.models.units import UnitUser
from radar.lib.roles import DISEASE_GROUP_ROLE_NAMES, UNIT_ROLE_NAMES
from radar.lib.user_search import UserQueryBuilder
from radar.lib.users import get_managed_units, get_managed_disease_groups, send_new_user_email
from radar.web.forms.users import DiseaseGroupRoleForm, UserSearchForm, UnitRoleForm, AddUserForm
from radar.models.users import User


ORDER_BY = {
    'id': User.id,
    'username': User.username,
    'email': User.email,
    'first_name': User.first_name,
    'last_name': User.last_name,
}


bp = Blueprint('users', __name__)


@bp.route('/')
def view_user_list():
    if not current_user.has_view_user_permission:
        abort(403)

    units = get_units_for_user_with_permissions(current_user, [UnitUser.has_view_user_permission])
    unit_choices = group_list_to_choices(units, include_blank=True)

    disease_groups = get_disease_groups_for_user_with_permissions(current_user, [DiseaseGroupUser.has_view_user_permission])
    disease_group_choices = group_list_to_choices(disease_groups, include_blank=True)

    form = UserSearchForm(formdata=request.args, csrf_enabled=False)
    form.unit_id.choices = unit_choices
    form.disease_group_id.choices = disease_group_choices

    builder = UserQueryBuilder(current_user)

    if form.validate():
        if form.username.data:
            builder.username(form.username.data)

        if form.email.data:
            builder.email(form.email.data)

        if form.first_name.data:
            builder.first_name(form.first_name.data)

        if form.last_name.data:
            builder.last_name(form.last_name.data)

        # Filter by disease group access
        if form.disease_group_id.data:
            builder.disease_group(form.disease_group_id.data)

        # Filter by unit access
        if form.unit_id.data:
            builder.unit(form.unit_id.data)

    query = builder.build()

    query, ordering = order_query(query, ORDER_BY, 'username')
    pagination = paginate_query(query)
    users = pagination.items

    users = [(x, get_user_data(x)) for x in users]

    context = dict(
        users=users,
        form=form,
        disease_groups=disease_groups,
        units=units,
        pagination=pagination,
        ordering=ordering,
    )

    return render_template('users.html', **context)


@bp.route('/<int:user_id>/', endpoint='view_user')
@bp.route('/<int:user_id>/', methods=['GET', 'POST'], endpoint='edit_user')
def view_user(user_id):
    user = User.query.get_or_404(user_id)

    if not user.can_view(current_user):
        abort(403)

    disease_group_form = get_disease_group_role_form()
    unit_form = get_unit_role_form()

    # TODO user role management
    if request.method == 'POST':
        if not user.can_edit_disease_group_roles(current_user):
            abort(403)

        if 'disease_group_submit' in request.form:
            if disease_group_form.validate():
                disease_group_id = disease_group_form.disease_group_id.data
                role = disease_group_form.role.data

                disease_group = DiseaseGroup.query.get_or_404(disease_group_id)

                # Get the user's current role
                disease_group_user = DiseaseGroupUser.query.filter(
                    DiseaseGroupUser.user == user,
                    DiseaseGroupUser.disease_group == disease_group
                ).first()

                # Adding user to disease group
                if disease_group_user is None:
                    if role:
                        disease_group_user = DiseaseGroupUser(user=user, disease_group=disease_group)
                else:
                    # Check we can make changes to the user's role
                    if not disease_group_user.can_edit(current_user):
                        abort(403)

                # Giving the user a new role
                if role:
                    # Update the role
                    disease_group_user.role = role

                    # Can we add the user to this role
                    if not disease_group_user.can_edit(current_user):
                        abort(403)

                    db.session.add(disease_group_user)
                    db.session.commit()
                elif disease_group_user is not None:
                    db.session.delete(disease_group_user)
                    db.session.commit()

                flash('Disease group role updated.', 'success')

                return redirect(url_for('users.view_user', user_id=user.id))

    context = dict(
        user=user,
        user_data=get_user_data(user),
        disease_group_form=disease_group_form,
        unit_form=unit_form,
    )

    return render_template('user.html', **context)


@bp.route('/add/', endpoint='add_user', methods=['GET', 'POST'])
def add_user():
    if not current_user.has_add_user_permission:
        abort(403)

    form = AddUserForm()

    if form.validate_on_submit():
        user = User()

        user.username = form.username.data.lower()
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        password = generate_password()
        user.set_initial_password(password)

        db.session.add(user)
        db.session.commit()

        send_new_user_email(user, password)

        message = (
            "User added successfully. "
            "An email has been sent to %s with the initial password and instructions on how to login. "
            "Don't forget to add the user to groups."
        ) % user.email

        flash(message, 'success')
        return redirect(url_for('users.edit_user', user_id=user.id))

    context = dict(
        form=form
    )

    return render_template('add_user.html', **context)


def get_user_data(user):
    units = sorted(user.filter_units_for_user(current_user), key=lambda x: x.unit.name.lower())
    disease_groups = sorted(user.filter_disease_groups_for_user(current_user), key=lambda x: x.disease_group.name.lower())

    return dict(
        units=units,
        disease_groups=disease_groups,
    )


def group_list_to_choices(groups, include_blank=False):
    choices = [(x.id, x.name) for x in groups]

    if include_blank:
        choices.insert(0, ('', ''))

    return choices


def role_list_to_choices(name_map, roles):
    choices = [('', 'No Access')]
    choices.extend([(x, name_map[x]) for x in roles])
    return choices


def get_unit_role_form():
    unit_form = UnitRoleForm()

    # Managed units
    units = get_managed_units(current_user)
    unit_form.unit_id.choices = group_list_to_choices(units)

    # Managed unit roles
    unit_roles = current_user.managed_unit_roles
    unit_form.role.choices = role_list_to_choices(UNIT_ROLE_NAMES, unit_roles)

    return unit_form


def get_disease_group_role_form():
    disease_group_form = DiseaseGroupRoleForm()

    # Managed disease groups
    disease_groups = get_managed_disease_groups(current_user)
    disease_group_form.disease_group_id.choices = group_list_to_choices(disease_groups)

    # Managed disease group roles
    disease_group_roles = current_user.managed_disease_group_roles
    disease_group_form.role.choices = role_list_to_choices(DISEASE_GROUP_ROLE_NAMES, disease_group_roles)

    return disease_group_form
