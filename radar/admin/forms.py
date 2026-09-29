from wtforms import fields, form, validators


class LoginForm(form.Form):
    username = fields.StringField(validators=[validators.DataRequired()])
    password = fields.PasswordField(validators=[validators.DataRequired()])
