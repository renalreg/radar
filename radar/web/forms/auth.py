from flask_login import current_user
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email

from radar.lib.auth import PASSWORD_POLICY
from radar.lib.auth import check_login
from radar.web.forms.core import radar_password_check


class LoginForm(Form):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])


class ForgotUsernameForm(Form):
    email = StringField(validators=[InputRequired()])


class ForgotPasswordForm(Form):
    username = StringField(validators=[InputRequired()])


class BaseChangePasswordForm(Form):
    new_password = PasswordField('New Password', description=PASSWORD_POLICY, validators=[InputRequired(), radar_password_check])
    new_password_confirm = PasswordField('Confirm New Password', validators=[InputRequired()])

    def validate(self):
        if not super(BaseChangePasswordForm, self).validate():
            return False

        valid = True

        if self.new_password.data != self.new_password_confirm.data:
            self.new_password_confirm.errors.append("Passwords don't match.")
            valid = False

        return valid


class ResetPasswordForm(BaseChangePasswordForm):
    pass


class AccountForm(Form):
    first_name = StringField(validators=[InputRequired()])
    last_name = StringField(validators=[InputRequired()])


class ChangePasswordForm(BaseChangePasswordForm):
    password = PasswordField('Current Password')

    def validate(self):
        if not super(ChangePasswordForm, self).validate():
            return False

        valid = True

        if not check_login(current_user.username, self.password.data):
            self.password.errors.append('Incorrect password.')
            valid = False

        if self.password.data == self.new_password.data:
            self.new_password.errors.append('Same as current password.')
            valid = False

        return valid



class ChangeEmailForm(Form):
    password = PasswordField('Current Password', validators=[InputRequired()])
    new_email = StringField('New Email', validators=[Email(), InputRequired()])
    new_email_confirm = StringField('Confirm New Email', validators=[Email(), InputRequired()])

    def validate(self):
        if not super(ChangeEmailForm, self).validate():
            return False

        valid = True

        if self.new_email.data != self.new_email_confirm.data:
            self.new_email_confirm.errors.append("Email addresses don't match.")
            valid = False

        return valid