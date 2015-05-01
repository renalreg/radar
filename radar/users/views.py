from flask import render_template, request, abort, Blueprint, flash, url_for, redirect, current_app
from flask_login import current_user, login_user, logout_user

from radar.database import db
from radar.disease_groups.services import get_disease_groups_for_user_with_permissions
from radar.disease_groups.models import DiseaseGroup
from radar.ordering import order_query
from radar.pagination import paginate_query
from radar.units.services import get_units_for_user_with_permissions
from radar.users.models import DiseaseGroupUser, UnitUser
from radar.users.roles import DISEASE_GROUP_ROLE_NAMES, UNIT_ROLE_NAMES
from radar.users.search import UserQueryBuilder
from radar.users.services import check_login, get_managed_units, get_managed_disease_groups
from radar.users.forms import DiseaseGroupRoleForm, LoginForm, UserSearchForm, UnitRoleForm
from radar.users.models import User


ORDER_BY = {
    'id': User.id,
    'username': User.username,
    'email': User.email,
}


bp = Blueprint('users', __name__)


@bp.route('/users/')
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


@bp.route('/users/<int:user_id>/', endpoint='view_user')
@bp.route('/users/<int:user_id>/', methods=['GET', 'POST'], endpoint='edit_user')
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


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = check_login(username, password)

        if user is not None:
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(request.args.get('next') or url_for('radar.index'))
        else:
            form.username.errors.append('Incorrect username or password.')

    return render_template('login.html', form=form)


@bp.route('/logout/', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('radar.index'))


def require_login():
    if request.endpoint not in ['radar.index', 'users.login', 'static'] and not current_user.is_authenticated():
        return current_app.login_manager.unauthorized()


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