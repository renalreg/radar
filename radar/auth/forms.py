from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


class LoginForm(Form):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])