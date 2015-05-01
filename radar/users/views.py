from flask import render_template, request, abort, Blueprint, flash, url_for, redirect, current_app
from flask_login import current_user, login_user, logout_user
from sqlalchemy import or_

from radar.database import db
from radar.disease_groups.services import get_disease_groups_for_user_with_permissions
from radar.disease_groups.models import DiseaseGroup
from radar.units.models import Unit
from radar.units.services import get_units_for_user_with_permissions
from radar.users.models import DiseaseGroupUser, UnitUser
from radar.users.search import UserQueryBuilder
from radar.users.services import check_login
from radar.users.forms import UserDiseaseGroupForm, LoginForm, UserSearchForm, UserUnitForm
from radar.users.models import User


bp = Blueprint('users', __name__)


def get_user_data(user):
    units = sorted(user.filter_units_for_user(current_user), key=lambda x: x.unit.name)
    disease_groups = sorted(user.filter_disease_groups_for_user(current_user), key=lambda x: x.disease_group.name)

    return dict(
        units=units,
        disease_groups=disease_groups,
    )


def group_list_to_choices(groups, include_blank=False):
    choices = [(x.id, x.name) for x in groups]

    if include_blank:
        choices.insert(0, ('', ''))

    return choices


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
    users = query.order_by(User.username).all()

    users = [(x, get_user_data(x)) for x in users]

    context = dict(
        users=users,
        form=form,
        disease_groups=disease_groups,
        units=units,
    )

    return render_template('users.html', **context)


@bp.route('/users/<int:user_id>/', methods=['GET'], endpoint='view_user')
@bp.route('/users/<int:user_id>/', methods=['GET'], endpoint='edit_user')
def view_user(user_id):
    user = User.query.get_or_404(user_id)

    if not user.can_view(current_user):
        abort(403)

    disease_group_form = UserDiseaseGroupForm()

    # TODO
    disease_group_form.disease_group_id.choices = group_list_to_choices(DiseaseGroup.query.all())
    disease_group_form.role.choices = [('', '')]

    unit_form = UserUnitForm()

    # TODO
    unit_form.unit_id.choices = group_list_to_choices(Unit.query.all())
    unit_form.role.choices = [('', '')]

    if request.form.get('disease_group_submit'):
        if disease_group_form.validate():
            disease_group_id = disease_group_form.disease_group_id.data
            role = disease_group_form.role.data

            disease_group = DiseaseGroup.query.get_or_404(disease_group_id)

            if update_user_disease_groups_permission(user, disease_group, role):
                abort(403)

            # Get the users' disease group membership
            disease_group_user = DiseaseGroupUser.query.filter(
                DiseaseGroupUser.user == user,
                DiseaseGroupUser.disease_group == disease_group
            ).first()

            # Update the user's disease group role
            if role:
                if disease_group_user is None:
                    disease_group_user = DiseaseGroupUser(user=user, disease_group=disease_group)
                    db.session.add(disease_group_user)

                # Set the user's role at the disease group
                disease_group_user.role = role
            else:
                # Remove the user from the disease group
                if disease_group_user is not None:
                    db.session.delete(disease_group_user)

            db.session.commit()

    context = dict(
        user=user,
        user_data=get_user_data(user),
        disease_group_form=disease_group_form,
        unit_form=unit_form
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