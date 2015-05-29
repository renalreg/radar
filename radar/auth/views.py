from datetime import datetime, timedelta

from flask import Blueprint, flash, redirect, request, url_for, render_template, current_app
from flask_login import login_user, logout_user, current_user

from radar.auth.constants import PUBLIC_ENDPOINTS, RESET_PASSWORD_MAX_AGE, FORCE_PASSWORD_CHANGE_ENDPOINTS
from radar.auth.forms import LoginForm, ResetPasswordForm, ForgotPasswordForm, ForgotUsernameForm, ChangeEmailForm, \
    ChangePasswordForm, AccountForm
from radar.auth.services import check_login, generate_reset_password_token, \
    send_reset_password_email, send_username_reminder_email
from radar.database import db
from radar.models.users import User


bp = Blueprint('auth', __name__)


def require_login():
    """ Makes sure the user is logged in """

    if request.endpoint not in PUBLIC_ENDPOINTS and not current_user.is_authenticated():
        return current_app.login_manager.unauthorized()


def force_password_change():
    if current_user.is_authenticated() and current_user.force_password_change and request.endpoint not in FORCE_PASSWORD_CHANGE_ENDPOINTS:
        flash('Please update your password.')
        return redirect(url_for('auth.change_password'))


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


@bp.route('/forgot-username/', methods=['GET', 'POST'], endpoint='forgot_username')
def forgot_username_view():
    form = ForgotUsernameForm()

    if form.validate_on_submit():
        email = form.email.data
        users = User.query.filter(User.email == form.email.data).order_by(User.username).all()

        if len(users) > 0:
            send_username_reminder_email(email, users)
            flash('A username reminder email has been sent.', 'success')
            return redirect(url_for('radar.index'))
        else:
            form.email.errors.append('Email not found.')

    context = dict(
        form=form,
    )

    return render_template('forgot_username.html', **context)


@bp.route('/forgot-password/', methods=['GET', 'POST'], endpoint='forgot_password')
def forgot_password_view():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user = User.query\
            .filter(User.username == form.username.data)\
            .first()

        if user is None:
            form.username.errors.append('Username not found.')
        else:
            token = generate_reset_password_token()
            user.reset_password_token = token
            user.reset_password_date = datetime.now()
            db.session.commit()

            send_reset_password_email(user, token)

            flash('A password reset email has been sent.', 'success')
            return redirect(url_for('radar.index'))

    context = dict(
        form=form,
    )

    return render_template('forgot_password.html', **context)


@bp.route('/reset-password/<token>/', methods=['GET', 'POST'], endpoint='reset_password')
def reset_password_view(token):
    user = User.query\
        .filter(User.reset_password_token == token)\
        .filter(User.reset_password_date >= datetime.now() - timedelta(seconds=RESET_PASSWORD_MAX_AGE))\
        .first()

    # Invalid token
    if user is None:
        flash('Sorry the password reset token is no longer valid.', 'error')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()

        flash('Password reset.', 'success')
        return redirect(url_for('auth.login'))

    context = dict(
        form=form,
    )

    return render_template('reset_password.html', **context)


@bp.route('/account/', methods=['GET', 'POST'], endpoint='account')
def account_view():
    account_form = AccountForm(prefix='account', obj=current_user)
    change_password_form = ChangePasswordForm(prefix='change-password')
    change_email_form = ChangeEmailForm(prefix='change-email')

    if 'account-submit' in request.form:
        if account_form.validate():
            current_user.first_name = account_form.first_name.data
            current_user.last_name = account_form.last_name.data
            db.session.commit()
            flash('Account updated.', 'success')
            return redirect(url_for('auth.account'))
    elif 'change-password-submit' in request.form:
        if change_password_form.validate():
            password = change_password_form.new_password.data
            current_user.set_password(password)
            db.session.commit()
            flash('Password updated.', 'success')
            return redirect(url_for('auth.account'))
    elif 'change-email-submit' in request.form:
        if change_email_form.validate():
            email = change_email_form.new_email.data
            current_user.email = email
            db.session.commit()
            flash('Email updated.', 'success')
            return redirect(url_for('auth.account'))

    context = dict(
        account_form=account_form,
        change_password_form=change_password_form,
        change_email_form=change_email_form,
    )

    return render_template('account.html', **context)


@bp.route('/change-password/', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        password = form.new_password.data
        current_user.set_password(password)
        db.session.commit()
        flash('Password updated.', 'success')
        return redirect(url_for('radar.index'))

    context = dict(
        form=form,
    )

    return render_template('change_password.html', **context)