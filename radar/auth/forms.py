from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email


class LoginForm(Form):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])


class ForgotUsernameForm(Form):
    email = StringField()


class ForgotPasswordForm(Form):
    username = StringField()


class ResetPasswordForm(Form):
    new_password = PasswordField()
    new_password_confirm = PasswordField()


class AccountForm(Form):
    first_name = StringField()
    last_name = StringField()


class ChangePasswordForm(Form):
    password = PasswordField('Current Passowrd')
    new_password = PasswordField('New Password')
    new_password_confirm = PasswordField('Confirm New Password')


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