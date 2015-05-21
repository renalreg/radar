from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email


class LoginForm(Form):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])


class ForgotUsernameForm(Form):
    email = StringField(validators=[InputRequired()])


class ForgotPasswordForm(Form):
    username = StringField(validators=[InputRequired()])


class BaseChangePasswordForm(Form):
    new_password = PasswordField('New Password', validators=[InputRequired()])
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