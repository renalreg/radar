from flask import render_template, flash, request, redirect, url_for
from flask.views import View
from flask_login import login_user, logout_user
from radar.authentication.forms import LoginForm
from radar.authentication.services import check_login


class LoginView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = LoginForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = check_login(username, password)

            if user is not None:
                login_user(user)
                flash('Logged in successfully.', 'success')
                return redirect(request.args.get('next') or url_for('index'))
            else:
                form.username.errors.append('Incorrect username or password.')

        print form.errors

        return render_template('login.html', form=form)


class LogoutView(View):
    def dispatch_request(self):
        logout_user()
        return redirect(url_for('index'))